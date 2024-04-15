<script>
    import { onMount } from 'svelte';
    let inputText = '';
  
    async function sendRequest() {
      if (inputText) {
        const response = await fetch(`http://localhost:8000/insight?topic=${encodeURIComponent(inputText)}`);
        const data = await response.json();
        console.log(data);
      }
    }
  
    function handleKeydown(event) {
      if (event.key === 'Enter') {
        sendRequest();
      }
    }
  </script>
  
  <input type="text" bind:value={inputText} on:keydown={handleKeydown} placeholder="Enter text and press Enter" />