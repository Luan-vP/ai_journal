<script>
    import InsightSearch from './InsightSearch.svelte';
    import JournallingEntry from './JournallingEntry.svelte';
</script>


<div class="container mx-auto px-4">
    <h1 class="text-4xl font-bold underline mb-4">
        Therapy App
    </h1>

    <p class="text-lg mb-2">What would you like to write about?</p>

    <div class="mb-4">
        <InsightSearch />
    </div>

    <p class="text-lg mb-2">Write your journal entry here:</p>

    <div class="mb-4">
        <JournallingEntry />
    </div>
</div>

<style lang="postcss">
    :global(html) {
        background-color: theme(colors.gray.100);
        font-size: 16px;
    }
</style>