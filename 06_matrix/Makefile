SCRIPTS  := $(sort $(filter-out _%.py, $(wildcard *.py)))
PERF     := $(patsubst %.py, perf/%.perf, $(SCRIPTS))
TIME     := $(patsubst %.py, time/%.time, $(SCRIPTS))
MEMIT    := $(patsubst %.py, memit/%.memit, $(SCRIPTS))
KERNPROF := $(patsubst %.py, kernprof/%.kernprof, $(SCRIPTS))

all: $(PERF) $(TIME) $(MEMIT) $(KERNPROF)

perf: $(PERF)

time: $(TIME)

memit: $(MEMIT)

kernprof: $(KERNPROF)

%.kernprof: %.py
	@echo "lineprof-izing $<"
	mkdir kernprof
	kernprof -l -v $< > $@ 2>&1

%.memit: %.py
	@echo "%memit-izing $<"
	mkdir memit
	python -m memory_profiler $< > $@ 2>&1

%.time: %.py
	@echo "Timing $<"
	mkdir time
	time -v python $< > $@ 2>&1

%.perf: %.py
	@echo "Perfiling $<"
	mkdir perf
	@perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,page-fault,minor-faults,cs,migrations python $< 2>&1 | sed 's/(\([0-9.]*%\))//g' > $@
	@grep 'seconds time' $@ | column -t | cut -f1 -d' '
	@grep 'cache-misses' $@ | column -t
	@echo ''

clean:
	rm -rf $(PERF) $(TIME) $(MEMIT) $(KERNPROF)
