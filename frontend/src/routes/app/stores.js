import { writable } from 'svelte/store';

export const load_layout = writable(true);
export const socket = writable(null);
export const profile = writable(null);