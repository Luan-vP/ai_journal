<script lang='ts'>
  import { onMount } from 'svelte';

  let inputText = '';
  let therapeutic_insight = '';

  
    async function sendRequest() {
        if (inputText) {
            const response = await fetch('http://localhost:8000/post_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text_input: inputText })
            });
            const data = await response.json();
            console.log(data);
            therapeutic_insight = data.message;
        }
    }
  
    function handleKeydown(event) {
      if (event.key === 'Enter') {
        sendRequest();
      }
    }

    function autoResize(event) {
        event.target.style.height = 'inherit';
        event.target.style.height = `${event.target.scrollHeight}px`;
    }
</script>

<div class="flex-col justify-center">
  {#if !therapeutic_insight}
  <div>
    <p class="text-lg mb-2 justify-center">Write your journal entry here:</p>
  </div>
  <div>
    <textarea class="w-2/3 px-3 py-2 border border-gray-300 rounded shadow-inner" bind:value={inputText} on:keydown={handleKeydown} on:input={autoResize} placeholder="Enter text and press Enter" />
  </div>
  {:else}
  <div>
    <p>{therapeutic_insight}</p>
  </div>
  {/if}
</div>
