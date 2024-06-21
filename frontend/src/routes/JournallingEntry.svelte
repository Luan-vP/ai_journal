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
      if (event.key === 'Enter' && !event.shiftKey) {
        sendRequest();
      }
    }

    function autoResize(event) {
        event.target.style.height = 'inherit';
        event.target.style.height = `${event.target.scrollHeight}px`;
    }
</script>

<div class="flex justify-center">
  <textarea class="w-2/3 px-3 py-2 border border-gray-300 rounded shadow-inner" bind:value={inputText} on:keydown={handleKeydown} on:input={autoResize} placeholder="Enter text and press Enter" />
  {#if therapeutic_insight}
    <br/>
    <p>Insight: {therapeutic_insight}</p>
  {/if}
</div>
