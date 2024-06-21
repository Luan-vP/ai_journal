<script>
    import { onMount } from 'svelte';
    let inputText = '';
    let writingPrompt = '';
  
    async function sendRequest() {
      if (inputText) {
        const response = await fetch(`http://localhost:8000/writing_prompt?therapy_topic=${encodeURIComponent(inputText)}`);
        const data = await response.json();
        console.log(data);
        writingPrompt = data.message;
      }
    }
  
    function handleKeydown(event) {
      if (event.key === 'Enter') {
        sendRequest();
      }
    }
  </script>
  
  <div class="flex-col justify-center">
    {#if !writingPrompt}
    <div class="w-2/3">
      <p class="text-lg mb-2 justify-center">What would you like to write about?</p>
    </div>
    <div class="w-2/3">
      <input class="px-3 py-2 border border-gray-300 rounded shadow-inner" type="text" bind:value={inputText} on:keydown={handleKeydown} placeholder="Enter text and press Enter" />
    </div>
    {:else}
    <div>
      <p class="mt-2">{writingPrompt}</p>
    </div>
    {/if}
  </div>