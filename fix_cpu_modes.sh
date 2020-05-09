#!/bin/bash

NO_TURBO=1
MODE=performance

if [[ "$1" == 'disable' ]]; then
    NO_TURBO=0
    MODE=powersave
fi

echo "Setting mode to: $MODE"
echo "Setting no_turbo to: $NO_TURBO"

for CPUFREQ in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor;
do
    [ -f $CPUFREQ ] || continue;
    echo -n $MODE > $CPUFREQ;
done

echo ${NO_TURBO} > /sys/devices/system/cpu/intel_pstate/no_turbo
