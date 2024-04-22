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
  
  <div>
    <input type="text" bind:value={inputText} on:keydown={handleKeydown} placeholder="Enter text and press Enter" />
    <p>{writingPrompt}</p>
  </div>