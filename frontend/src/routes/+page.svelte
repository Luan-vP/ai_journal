<script>
    import InsightSearch from './InsightSearch.svelte';
    import JournallingEntry from './JournallingEntry.svelte';
    import Timer from './Timer.svelte';

    let countdown = 600;
</script>


<div class="container mx-auto px-4">
    <h1 class="text-4xl font-bold underline mb-4 justify-center">
        Therapy App
    </h1>

    <div class="mb-4 justify-center">
        <InsightSearch />
    </div>

    <div class="w-1/6 mb-10 justify-center">
        {#if countdown}
          <Timer {countdown} />
        {/if}
    </div>

    <div class="mb-4 justify-center">
        <JournallingEntry />
    </div>
</div>

<style lang="postcss">
    :global(html) {
        background-color: theme(colors.gray.100);
        font-size: 16px;
    }

</style>