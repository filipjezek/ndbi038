export function promiseTimeout(timeout: number) {
  return new Promise<void>((res, rej) => {
    setTimeout(() => {
      res();
    }, timeout);
  });
}
