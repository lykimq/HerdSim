import { Assets } from 'pixi.js';
import { icons } from '../assets/icons.js';
import { log, withTimeout } from '../utils/logger.js';

let cache = null;
let loading = null;

/** Load agent/field icon textures once and reuse across Single + Arena canvases. */
export async function loadIconTextures() {
  if (cache) return cache;
  if (loading) return loading;

  loading = (async () => {
    log.info('textures', 'Loading shared Game Icons textures');
    const started = performance.now();
    try {
      const [sheep, dog, shepherd, goal, pen] = await withTimeout(
        Promise.all([
          Assets.load({ src: icons.sheep, data: { resolution: 3 } }),
          Assets.load({ src: icons.dog, data: { resolution: 3 } }),
          Assets.load({ src: icons.shepherd, data: { resolution: 3 } }),
          Assets.load({ src: icons.goal, data: { resolution: 3 } }),
          Assets.load({ src: icons.pen, data: { resolution: 2 } }),
        ]),
        20000,
        'icon texture load',
      );
      cache = { sheep, dog, shepherd, goal, pen };
      log.info(
        'textures',
        `Textures ready in ${Math.round(performance.now() - started)}ms`,
      );
      return cache;
    } catch (err) {
      loading = null;
      log.error('textures', err.message || String(err), err);
      throw err;
    }
  })();

  return loading;
}
