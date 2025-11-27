import { writable } from 'svelte/store';

export const load_server_navbnar = writable(true);
export const socket = writable(null);
export const profile = writable({});