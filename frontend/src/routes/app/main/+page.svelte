<script>
	import { onMount } from "svelte";
  import { profile, socket } from "../stores";

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms)); 

  // onMount(async () => {
  //   let connected = false;
  //   let tries = 0;
  //   while(!connected) {
  //       if($socket?.readyState === WebSocket.OPEN)connected = true;
  //       tries += 1;
  //       if(tries > 3) {
  //           window.location.pathname = "/login"
  //           return;
  //       };
  //       console.warn("Not connected to the web socket. Retrying in 1 second...");

  //       await sleep(1000)
  //   }
  // });

</script>



<style>

</style>