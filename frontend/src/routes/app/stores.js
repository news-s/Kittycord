import { writable } from 'svelte/store';

export const load_server_bar = writable(true);
export const socket = writable(null);
export const profile = writable(null);