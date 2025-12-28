// CSC Latin America 2026 - Event Processor Benchmarks
#include <benchmark/benchmark.h>
#include "EventProcessor.hpp"

using namespace csc2026;

static void BM_GenerateEvents(benchmark::State& state) {
    const int nEvents = state.range(0);
    for (auto _ : state) {
        auto events = generateSampleEvents(nEvents, 10);
        benchmark::DoNotOptimize(events);
    }
    state.SetItemsProcessed(state.iterations() * nEvents);
}
BENCHMARK(BM_GenerateEvents)->Range(100, 10000);

static void BM_ProcessEventsSequential(benchmark::State& state) {
    const int nEvents = state.range(0);
    auto events = generateSampleEvents(nEvents, 50);
    
    for (auto _ : state) {
        EventProcessor processor;
        for (const auto& event : events) {
            processor.processEvent(event);
        }
        benchmark::DoNotOptimize(processor.totalEnergy());
    }
    state.SetItemsProcessed(state.iterations() * nEvents);
}
BENCHMARK(BM_ProcessEventsSequential)->Range(100, 10000);

static void BM_ProcessEventsParallel(benchmark::State& state) {
    const int nEvents = state.range(0);
    auto events = generateSampleEvents(nEvents, 50);
    
    for (auto _ : state) {
        EventProcessor processor;
        processor.processEvents(events);
        benchmark::DoNotOptimize(processor.totalEnergy());
    }
    state.SetItemsProcessed(state.iterations() * nEvents);
}
BENCHMARK(BM_ProcessEventsParallel)->Range(100, 10000);

// Benchmark the overhead of creating Event objects
static void BM_EventCreation(benchmark::State& state) {
    for (auto _ : state) {
        Event event;
        event.eventNumber = 42;
        event.particles.reserve(100);
        for (int i = 0; i < 100; ++i) {
            event.particles.emplace_back(i * 0.1, i * 0.2, i * 0.3, 0.139);
        }
        benchmark::DoNotOptimize(event);
    }
}
BENCHMARK(BM_EventCreation);

// Benchmark track reconstruction
static void BM_TrackReconstruction(benchmark::State& state) {
    Event event;
    event.particles.reserve(100);
    for (int i = 0; i < 100; ++i) {
        event.particles.emplace_back(i * 0.1, i * 0.2, i * 0.3, 0.139);
    }
    
    for (auto _ : state) {
        auto tracks = event.reconstructTracks();
        benchmark::DoNotOptimize(tracks);
    }
}
BENCHMARK(BM_TrackReconstruction);
