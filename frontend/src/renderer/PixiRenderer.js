import { Application, Container, Graphics, Sprite, Text } from 'pixi.js';
import { loadIconTextures } from './iconTextures.js';
import { log } from '../utils/logger.js';

/** Major grid spacing in world units (simulation meters / paper units). */
const GRID_MAJOR = 25;
/** Minor grid spacing in world units. */
const GRID_MINOR = 5;
/** Axis label step (keep sparse for performance). */
const LABEL_STEP = 50;

/**
 * PixiJS renderer for the herding field, goal, obstacles, and agents.
 *
 * Display convention: world origin (0,0) is bottom-left (scientific / plot style).
 * The decorative grid marks world units; it is not a simulation lattice.
 */
export class PixiRenderer {
  constructor(hostEl) {
    this.hostEl = hostEl;
    this.app = null;
    this.fieldLayer = null;
    this.agentLayer = null;
    this.overlayLayer = null;
    this.textures = { sheep: null, dog: null, shepherd: null, goal: null, pen: null };
    this.herderKind = 'dog';
    this.world = {
      width: 150,
      height: 150,
      goal_center: [15, 15],
      goal_radius: 15,
      obstacles: [],
    };
    this._ready = false;
  }

  async init() {
    log.info('pixi', 'Initializing renderer');
    try {
      this.app = new Application();
      await this.app.init({
        background: '#090d16',
        antialias: true,
        resizeTo: this.hostEl,
        // Prefer canvas2d fallback path avoidance; one WebGL context per view.
        preference: 'webgl',
      });
      this.hostEl.innerHTML = '';
      this.hostEl.appendChild(this.app.canvas);

      this.fieldLayer = new Container();
      this.agentLayer = new Container();
      this.overlayLayer = new Container();
      this.app.stage.addChild(this.fieldLayer);
      this.app.stage.addChild(this.agentLayer);
      this.app.stage.addChild(this.overlayLayer);

      this.textures = await loadIconTextures();
      this._ready = true;
      this.app.renderer.on('resize', () => {
        if (this._ready) this._drawField();
      });
      this._drawField();
      log.info('pixi', 'Renderer ready', {
        w: this.app.renderer.width,
        h: this.app.renderer.height,
      });
    } catch (err) {
      log.error('pixi', err.message || String(err), err);
      this.hostEl.innerHTML =
        `<div class="canvas-error">Renderer failed: ${err.message || err}</div>`;
      throw err;
    }
  }

  setWorld(world) {
    if (!world) return;
    this.world = {
      width: world.width ?? 150,
      height: world.height ?? 150,
      goal_center: world.goal_center ?? [15, 15],
      goal_radius: world.goal_radius ?? 15,
      obstacles: world.obstacles ?? [],
    };
    if (this._ready) this._drawField();
  }

  setHerderKind(kind) {
    this.herderKind = kind === 'human' ? 'human' : 'dog';
  }

  _herderTexture() {
    return this.herderKind === 'human' ? this.textures.shepherd : this.textures.dog;
  }

  _scale() {
    const w = this.app.renderer.width;
    const h = this.app.renderer.height;
    // Leave a small margin for axis labels.
    const pad = 28;
    const s = Math.min(
      (w - pad * 1.5) / this.world.width,
      (h - pad * 1.5) / this.world.height,
    );
    const offsetX = pad + (w - pad * 1.5 - this.world.width * s) / 2;
    const offsetY = (h - pad - this.world.height * s) / 2;
    return { s, offsetX, offsetY, w, h, pad };
  }

  /** Map world (x,y) with origin bottom-left to screen pixels. */
  _toScreen(x, y) {
    const { s, offsetX, offsetY } = this._scale();
    return [offsetX + x * s, offsetY + (this.world.height - y) * s];
  }

  _placeSprite(texture, x, y, size) {
    const sprite = new Sprite(texture);
    sprite.anchor.set(0.5);
    sprite.width = size;
    sprite.height = size;
    sprite.position.set(x, y);
    return sprite;
  }

  _makeLabel(text, x, y, opts = {}) {
    const label = new Text({
      text,
      style: {
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: opts.size || 10,
        fill: opts.fill || 0x94a3b8,
        fontWeight: opts.bold ? '600' : '400',
      },
    });
    label.anchor.set(opts.ax ?? 0.5, opts.ay ?? 0.5);
    label.position.set(x, y);
    label.alpha = opts.alpha ?? 0.9;
    return label;
  }

  _drawField() {
    if (!this._ready || !this.app?.renderer) return;
    this.fieldLayer.removeChildren();
    this.overlayLayer.removeChildren();
    const { s, offsetX, offsetY, pad, w, h } = this._scale();
    if (w < 40 || h < 40) {
      log.debug('pixi', 'Skip field draw; canvas not laid out yet', { w, h });
      return;
    }
    const fieldW = this.world.width * s;
    const fieldH = this.world.height * s;
    const g = new Graphics();

    g.rect(0, 0, this.app.renderer.width, this.app.renderer.height);
    g.fill({ color: 0x090d16 });

    // Pasture / arena fill
    g.rect(offsetX, offsetY, fieldW, fieldH);
    g.fill({ color: 0x102018 });

    // Minor grid
    g.setStrokeStyle({ width: 1, color: 0xffffff, alpha: 0.04 });
    for (let x = 0; x <= this.world.width + 0.01; x += GRID_MINOR) {
      if (x % GRID_MAJOR === 0) continue;
      const [sx] = this._toScreen(x, 0);
      g.moveTo(sx, offsetY);
      g.lineTo(sx, offsetY + fieldH);
    }
    for (let y = 0; y <= this.world.height + 0.01; y += GRID_MINOR) {
      if (y % GRID_MAJOR === 0) continue;
      const [, sy] = this._toScreen(0, y);
      g.moveTo(offsetX, sy);
      g.lineTo(offsetX + fieldW, sy);
    }
    g.stroke();

    // Major grid (world units)
    g.setStrokeStyle({ width: 1, color: 0xffffff, alpha: 0.12 });
    for (let x = 0; x <= this.world.width + 0.01; x += GRID_MAJOR) {
      const [sx] = this._toScreen(x, 0);
      g.moveTo(sx, offsetY);
      g.lineTo(sx, offsetY + fieldH);
    }
    for (let y = 0; y <= this.world.height + 0.01; y += GRID_MAJOR) {
      const [, sy] = this._toScreen(0, y);
      g.moveTo(offsetX, sy);
      g.lineTo(offsetX + fieldW, sy);
    }
    g.stroke();

    // Field border
    g.setStrokeStyle({ width: 2, color: 0xcbd5e1, alpha: 0.55 });
    g.rect(offsetX, offsetY, fieldW, fieldH);
    g.stroke();

    this.fieldLayer.addChild(g);

    // Axis tick labels (world units) -- sparse for readability/perf
    for (let x = 0; x <= this.world.width + 0.01; x += LABEL_STEP) {
      const [sx] = this._toScreen(x, 0);
      this.overlayLayer.addChild(
        this._makeLabel(String(x), sx, offsetY + fieldH + 10, { size: 9, ay: 0 }),
      );
    }
    for (let y = 0; y <= this.world.height + 0.01; y += LABEL_STEP) {
      const [, sy] = this._toScreen(0, y);
      this.overlayLayer.addChild(
        this._makeLabel(String(y), offsetX - 8, sy, { size: 9, ax: 1 }),
      );
    }
    this.overlayLayer.addChild(
      this._makeLabel('x', offsetX + fieldW / 2, offsetY + fieldH + 20, {
        size: 10,
        fill: 0x64748b,
      }),
    );
    this.overlayLayer.addChild(
      this._makeLabel('y', Math.max(10, offsetX - pad + 4), offsetY + fieldH / 2, {
        size: 10,
        fill: 0x64748b,
        ax: 0.5,
      }),
    );

    // Scale bar (one major cell)
    const barWorld = GRID_MAJOR;
    const barPx = barWorld * s;
    const barX = offsetX + fieldW - barPx - 12;
    const barY = offsetY + 14;
    const bar = new Graphics();
    bar.setStrokeStyle({ width: 2, color: 0xe2e8f0, alpha: 0.85 });
    bar.moveTo(barX, barY);
    bar.lineTo(barX + barPx, barY);
    bar.moveTo(barX, barY - 4);
    bar.lineTo(barX, barY + 4);
    bar.moveTo(barX + barPx, barY - 4);
    bar.lineTo(barX + barPx, barY + 4);
    bar.stroke();
    this.overlayLayer.addChild(bar);
    this.overlayLayer.addChild(
      this._makeLabel(`${barWorld} units`, barX + barPx / 2, barY + 10, {
        size: 9,
        fill: 0xe2e8f0,
      }),
    );

    for (const obs of this.world.obstacles) {
      const [x0, y0] = obs.min_corner;
      const [x1, y1] = obs.max_corner;
      const [sx0, sy0] = this._toScreen(x0, y1);
      const [sx1, sy1] = this._toScreen(x1, y0);
      const ow = Math.abs(sx1 - sx0);
      const oh = Math.abs(sy1 - sy0);
      const cx = (sx0 + sx1) / 2;
      const cy = (sy0 + sy1) / 2;
      if (this.textures.pen) {
        const fence = this._placeSprite(this.textures.pen, cx, cy, Math.min(ow, oh));
        fence.width = ow;
        fence.height = oh;
        this.fieldLayer.addChild(fence);
      } else {
        const box = new Graphics();
        box.rect(Math.min(sx0, sx1), Math.min(sy0, sy1), ow, oh);
        box.fill({ color: 0x8e644b, alpha: 0.9 });
        this.fieldLayer.addChild(box);
      }
    }

    if (this.world.goal_center && this.world.goal_radius != null) {
      const [gx, gy] = this.world.goal_center;
      const [sx, sy] = this._toScreen(gx, gy);
      const gr = this.world.goal_radius * s;
      const ring = new Graphics();
      ring.circle(sx, sy, gr);
      ring.fill({ color: 0xd13438, alpha: 0.14 });
      ring.setStrokeStyle({ width: 2, color: 0xd13438, alpha: 0.95 });
      ring.circle(sx, sy, gr);
      ring.stroke();
      // Dashed inner guide
      ring.setStrokeStyle({ width: 1, color: 0xfca5a5, alpha: 0.7 });
      ring.circle(sx, sy, Math.max(4, gr * 0.55));
      ring.stroke();
      this.fieldLayer.addChild(ring);
      if (this.textures.goal) {
        const marker = this._placeSprite(
          this.textures.goal,
          sx,
          sy,
          Math.max(14, Math.min(gr * 0.55, 32)),
        );
        this.fieldLayer.addChild(marker);
      }
      this.overlayLayer.addChild(
        this._makeLabel('GOAL', sx, sy - gr - 8, {
          size: 11,
          fill: 0xfca5a5,
          bold: true,
        }),
      );
    }
  }

  render(frame) {
    if (!this._ready || !frame) return;
    if (frame.world) this.setWorld(frame.world);

    this.agentLayer.removeChildren();
    const sheep = frame.sheep_positions || [];
    const dogs = frame.shepherd_positions || [];
    const { s } = this._scale();
    const sheepSize = Math.max(10, 7.5 * s);
    const dogSize = Math.max(12, 9 * s);

    sheep.forEach(([x, y]) => {
      const [px, py] = this._toScreen(x, y);
      if (this.textures.sheep) {
        this.agentLayer.addChild(this._placeSprite(this.textures.sheep, px, py, sheepSize));
      } else {
        const g = new Graphics();
        g.circle(px, py, sheepSize * 0.35);
        g.fill({ color: 0xffffff });
        this.agentLayer.addChild(g);
      }
    });

    dogs.forEach(([x, y]) => {
      const [px, py] = this._toScreen(x, y);
      const tex = this._herderTexture();
      if (tex) {
        this.agentLayer.addChild(this._placeSprite(tex, px, py, dogSize));
      } else {
        const g = new Graphics();
        g.circle(px, py, dogSize * 0.35);
        g.fill({ color: this.herderKind === 'human' ? 0x76a04d : 0xfbbf24 });
        this.agentLayer.addChild(g);
      }
    });
  }

  destroy() {
    if (this.app) {
      // Keep shared icon textures alive for the next view mount.
      this.app.destroy(
        { removeView: true },
        { children: true, texture: false, textureSource: false },
      );
      this.app = null;
    }
    this._ready = false;
    log.debug('pixi', 'Renderer destroyed');
  }
}
