#!/usr/bin/env bash
set -u
set -o pipefail

usage() {
    cat <<'TEXT'
Usage: ./check_all.sh [SOURCE_DIRECTORY] [BUILD_DIRECTORY]
Defaults: ./src and ./build beside this script.
Environment: CXX=/path/to/g++-14, RUN_TIMEOUT=30s, MEMORY_TIMEOUT=90s
Exit codes: 0 = all checks passed; 1 = a check failed; 2 = incomplete verification.
Normal executables: BUILD_DIRECTORY/bin/
Sanitized executables: BUILD_DIRECTORY/sanitized/
Logs and summary: BUILD_DIRECTORY/logs/, BUILD_DIRECTORY/summary.tsv
Requires Bash, a C++23 compiler with <print>, and GNU timeout.
Leak checks use LeakSanitizer or, if unavailable, Valgrind.
TEXT
}

if [[ ${1:-} == --help || ${1:-} == -h ]]; then
    usage
    exit 0
fi
if (( $# > 2 )); then
    usage >&2
    exit 2
fi

SCRIPT_DIRECTORY=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd) || exit 2
SOURCE_DIRECTORY=${1:-"$SCRIPT_DIRECTORY/src"}
BUILD_DIRECTORY=${2:-"$SCRIPT_DIRECTORY/build"}
RUN_TIMEOUT=${RUN_TIMEOUT:-30s}
MEMORY_TIMEOUT=${MEMORY_TIMEOUT:-90s}

for utility in find sort timeout tr wc grep mktemp; do
    if ! command -v "$utility" >/dev/null 2>&1; then
        printf 'Missing required utility: %s\n' "$utility" >&2
        exit 2
    fi
done
if [[ ! -d $SOURCE_DIRECTORY ]]; then
    printf 'Source directory does not exist: %s\n' "$SOURCE_DIRECTORY" >&2
    exit 2
fi
SOURCE_DIRECTORY=$(cd -- "$SOURCE_DIRECTORY" && pwd) || exit 2
mkdir -p -- "$BUILD_DIRECTORY/bin" "$BUILD_DIRECTORY/sanitized" "$BUILD_DIRECTORY/logs" || exit 2
BUILD_DIRECTORY=$(cd -- "$BUILD_DIRECTORY" && pwd) || exit 2

if [[ -z ${CXX:-} ]]; then
    for candidate in g++-15 g++-14 g++ clang++; do
        if command -v "$candidate" >/dev/null 2>&1; then
            CXX=$candidate
            break
        fi
    done
fi
if [[ -z ${CXX:-} ]] || ! command -v "$CXX" >/dev/null 2>&1; then
    printf 'No compiler found. Set CXX to a C++23 compiler executable.\n' >&2
    exit 2
fi

mapfile -d '' -t SOURCES < <(find "$SOURCE_DIRECTORY" -maxdepth 1 -type f -name '*.cpp' -print0 | sort -z)
if (( ${#SOURCES[@]} == 0 )); then
    printf 'No .cpp files in %s\n' "$SOURCE_DIRECTORY" >&2
    exit 2
fi

COMMON_FLAGS=(-std=c++23 -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
NORMAL_FLAGS=(-O2 -g)
SANITIZER_FLAGS=(-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -fno-pie -no-pie)
SUMMARY="$BUILD_DIRECTORY/summary.tsv"
printf 'file\tascii\tcompile\trun\tsanitizer_compile\tasan_ubsan\tleaks\n' > "$SUMMARY" || exit 2
TEMP_DIRECTORY=$(mktemp -d "$BUILD_DIRECTORY/.check-all.XXXXXXXX") || exit 2
trap 'rm -rf -- "$TEMP_DIRECTORY"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

"$CXX" --version > "$BUILD_DIRECTORY/logs/compiler.txt" 2>&1
printf 'Compiler: %s\nSources: %s\nBuild: %s\n' "$CXX" "$SOURCE_DIRECTORY" "$BUILD_DIRECTORY"
printf 'Flags: %s\n' "${COMMON_FLAGS[*]}"

cat > "$TEMP_DIRECTORY/leak_probe.cpp" <<'CPP'
#include <cstdio>

void leak()
{
    int* values = new int[8]{};
    std::printf("%p\n", static_cast<void*>(values));
}

int main()
{
    leak();
}
CPP

LEAK_BACKEND=unavailable
if "$CXX" "${COMMON_FLAGS[@]}" -O0 -g -fsanitize=address,undefined -fno-pie -no-pie \
    "$TEMP_DIRECTORY/leak_probe.cpp" -o "$TEMP_DIRECTORY/leak_probe_sanitized" \
    > "$BUILD_DIRECTORY/logs/leak-probe-build.log" 2>&1; then
    ASAN_OPTIONS=detect_leaks=1:halt_on_error=1:exitcode=23 \
    LSAN_OPTIONS=exitcode=23 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
    timeout --kill-after=2s "$MEMORY_TIMEOUT" "$TEMP_DIRECTORY/leak_probe_sanitized" \
    > "$BUILD_DIRECTORY/logs/leak-probe.log" 2>&1
    probe_status=$?
    if (( probe_status == 23 )) && grep -q 'LeakSanitizer: detected memory leaks' "$BUILD_DIRECTORY/logs/leak-probe.log"; then
        LEAK_BACKEND=lsan
    fi
fi

if [[ $LEAK_BACKEND == unavailable ]] && command -v valgrind >/dev/null 2>&1; then
    if "$CXX" "${COMMON_FLAGS[@]}" -O0 -g "$TEMP_DIRECTORY/leak_probe.cpp" \
        -o "$TEMP_DIRECTORY/leak_probe_normal" > "$BUILD_DIRECTORY/logs/valgrind-probe-build.log" 2>&1; then
        timeout --kill-after=2s "$MEMORY_TIMEOUT" valgrind --leak-check=full \
            --show-leak-kinds=all --errors-for-leak-kinds=definite,indirect,possible \
            --error-exitcode=23 "$TEMP_DIRECTORY/leak_probe_normal" \
            > "$BUILD_DIRECTORY/logs/valgrind-probe.log" 2>&1
        probe_status=$?
        if (( probe_status == 23 )) && grep -Eq 'definitely lost: [1-9][0-9,]* bytes' "$BUILD_DIRECTORY/logs/valgrind-probe.log"; then
            LEAK_BACKEND=valgrind
        fi
    fi
fi
printf 'Leak-check backend: %s\n' "$LEAK_BACKEND"
if [[ $LEAK_BACKEND == unavailable ]]; then
    printf 'WARNING: leak detection is unavailable. Verification cannot receive a full PASS.\n' >&2
    printf 'See leak-probe logs; install Valgrind or use a system where LeakSanitizer works.\n' >&2
fi
printf 'leak_backend=%s\nrun_timeout=%s\nmemory_timeout=%s\n' \
    "$LEAK_BACKEND" "$RUN_TIMEOUT" "$MEMORY_TIMEOUT" > "$BUILD_DIRECTORY/logs/settings.txt"

prepare_input() {
    case "$1" in
        02.01) printf '10\n' ;;
        02.02) printf '1 -3 2\n' ;;
        02.03) printf 'Az5! \n' ;;
        02.04|02.08|02.09|02.10|03.01|03.02|03.03|03.04|03.05|03.06) : ;;
        02.05) printf '0.001\n' ;;
        02.06) printf '4 4 1 3 2\n' ;;
        02.07) printf '4 1 3 2\n' ;;
        *) return 1 ;;
    esac
}

FAILED=0
INCOMPLETE=0
if [[ $LEAK_BACKEND == unavailable ]]; then
    INCOMPLETE=1
fi

for source in "${SOURCES[@]}"; do
    name=${source##*/}
    stem=${name%.cpp}
    executable="$BUILD_DIRECTORY/bin/$stem"
    sanitized="$BUILD_DIRECTORY/sanitized/$stem"
    log_prefix="$BUILD_DIRECTORY/logs/$stem"
    input="$TEMP_DIRECTORY/$stem.in"
    ascii_status=PASS
    compile_status=FAIL
    run_status=SKIP
    sanitizer_compile_status=FAIL
    sanitizer_status=SKIP
    leak_status=SKIP

    non_ascii=$(LC_ALL=C tr -d '\000-\177' < "$source" | wc -c)
    if (( non_ascii != 0 )); then
        ascii_status=FAIL
        FAILED=1
    fi

    if "$CXX" "${COMMON_FLAGS[@]}" "${NORMAL_FLAGS[@]}" "$source" -o "$TEMP_DIRECTORY/normal" \
        > "$log_prefix.compile.log" 2>&1; then
        if mv -f -- "$TEMP_DIRECTORY/normal" "$executable"; then
            compile_status=PASS
        else
            FAILED=1
        fi
    else
        FAILED=1
    fi
    if [[ $compile_status != PASS ]]; then
        rm -f -- "$executable"
    fi

    if "$CXX" "${COMMON_FLAGS[@]}" "${SANITIZER_FLAGS[@]}" "$source" -o "$TEMP_DIRECTORY/sanitized" \
        > "$log_prefix.sanitizer-compile.log" 2>&1; then
        if mv -f -- "$TEMP_DIRECTORY/sanitized" "$sanitized"; then
            sanitizer_compile_status=PASS
        else
            FAILED=1
        fi
    else
        FAILED=1
    fi
    if [[ $sanitizer_compile_status != PASS ]]; then
        rm -f -- "$sanitized"
    fi

    if ! prepare_input "$stem" > "$input"; then
        printf '%s: no input scenario; compiled, automatic execution skipped.\n' "$name" >&2
        INCOMPLETE=1
    else
        if [[ $compile_status == PASS ]]; then
            timeout --kill-after=2s "$RUN_TIMEOUT" "$executable" < "$input" \
                > "$log_prefix.run.stdout" 2> "$log_prefix.run.stderr"
            status=$?
            printf '%s\n' "$status" > "$log_prefix.run.exit"
            if (( status == 0 )); then
                run_status=PASS
            else
                run_status="FAIL($status)"
                FAILED=1
            fi
        fi
        if [[ $sanitizer_compile_status == PASS ]]; then
            detect_leaks=0
            if [[ $LEAK_BACKEND == lsan ]]; then
                detect_leaks=1
            fi
            ASAN_OPTIONS="detect_leaks=$detect_leaks:halt_on_error=1:exitcode=99" \
            LSAN_OPTIONS=exitcode=99 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
            timeout --kill-after=2s "$MEMORY_TIMEOUT" "$sanitized" < "$input" \
                > "$log_prefix.sanitizer.stdout" 2> "$log_prefix.sanitizer.stderr"
            status=$?
            printf '%s\n' "$status" > "$log_prefix.sanitizer.exit"
            if (( status == 0 )); then
                sanitizer_status=PASS
                if [[ $LEAK_BACKEND == lsan ]]; then
                    leak_status=PASS
                fi
            else
                sanitizer_status="FAIL($status)"
                if [[ $LEAK_BACKEND == lsan ]]; then
                    leak_status=UNVERIFIED
                fi
                FAILED=1
            fi
        fi
        if [[ $LEAK_BACKEND == valgrind && $compile_status == PASS ]]; then
            timeout --kill-after=2s "$MEMORY_TIMEOUT" valgrind --leak-check=full \
                --show-leak-kinds=all --errors-for-leak-kinds=definite,indirect,possible \
                --track-origins=yes --error-exitcode=99 "$executable" < "$input" \
                > "$log_prefix.valgrind.stdout" 2> "$log_prefix.valgrind.stderr"
            status=$?
            printf '%s\n' "$status" > "$log_prefix.valgrind.exit"
            if (( status == 0 )); then
                leak_status=PASS
            else
                leak_status="FAIL($status)"
                FAILED=1
            fi
        fi
        if [[ $LEAK_BACKEND == unavailable ]]; then
            leak_status=UNAVAILABLE
        fi
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$ascii_status" "$compile_status" \
        "$run_status" "$sanitizer_compile_status" "$sanitizer_status" "$leak_status" >> "$SUMMARY"
    printf '%s: ASCII=%s compile=%s run=%s sanitizer_build=%s ASan/UBSan=%s leaks=%s\n' \
        "$name" "$ascii_status" "$compile_status" "$run_status" \
        "$sanitizer_compile_status" "$sanitizer_status" "$leak_status"
done

printf '\nNormal executables: %s/bin/\nSummary: %s\nLogs: %s/logs/\n' \
    "$BUILD_DIRECTORY" "$SUMMARY" "$BUILD_DIRECTORY"
if (( FAILED )); then
    printf 'FAIL: at least one check failed. Inspect the per-file logs.\n' >&2
    exit 1
fi
if (( INCOMPLETE )); then
    printf 'INCOMPLETE: compilation/execution may pass, but some checks were unavailable or skipped.\n' >&2
    exit 2
fi
printf 'PASS: all configured checks passed for the supplied execution scenarios.\n'
