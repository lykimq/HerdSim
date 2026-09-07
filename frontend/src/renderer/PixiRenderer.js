import { Application, Container, Graphics, Sprite, Text } from 'pixi.js';
import { loadIconTextures } from './iconTextures.js';
import { drawField } from './drawField.js';
import { log } from '../utils/logger.js';

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
    drawField(this);
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

    this._drawAssignmentOverlay(frame);
  }

  _drawAssignmentOverlay(frame) {
    this.overlayLayer.removeChildren();
    const lines = frame?.metadata?.assignment_lines;
    if (!Array.isArray(lines) || lines.length === 0) return;

    const g = new Graphics();
    lines.forEach((line) => {
      const from = line?.from;
      const to = line?.to;
      if (!Array.isArray(from) || !Array.isArray(to)) return;
      const [x1, y1] = this._toScreen(from[0], from[1]);
      const [x2, y2] = this._toScreen(to[0], to[1]);
      const collect = line.mode === 'collect';
      g.moveTo(x1, y1);
      g.lineTo(x2, y2);
      g.stroke({
        width: collect ? 1.6 : 1.1,
        color: collect ? 0xfbbf24 : 0x67e8f9,
        alpha: collect ? 0.85 : 0.45,
      });
    });
    this.overlayLayer.addChild(g);
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
