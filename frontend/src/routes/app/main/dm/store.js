import { writable } from "svelte/store";

export const friends = writable([]);    
export const messages = writable([]);   
export const activeDM = writable(null); 
