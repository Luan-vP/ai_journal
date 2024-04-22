<script>
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
                body: JSON.stringify({ journal_entry: inputText })
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
  </script>

<div>
  <input type="text" bind:value={inputText} on:keydown={handleKeydown} placeholder="Enter text and press Enter" />
    <p>Insight:{therapeutic_insight}</p>
</div>