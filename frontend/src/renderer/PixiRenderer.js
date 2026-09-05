import { Application, Container, Graphics, Sprite, Assets } from 'pixi.js';
import sheepUrl from '../assets/sheep_sprite.svg';
import dogUrl from '../assets/dog_sprite.svg';

/**
 * PixiJS renderer for the herding field, goal, obstacles, and agents.
 * World dimensions and goal come from backend websocket frames.
 */
export class PixiRenderer {
  constructor(hostEl) {
    this.hostEl = hostEl;
    this.app = null;
    this.fieldLayer = null;
    this.agentLayer = null;
    this.sheepSprites = [];
    this.dogSprites = [];
    this.sheepTexture = null;
    this.dogTexture = null;
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
    this.app = new Application();
    await this.app.init({
      background: '#090d16',
      antialias: true,
      resizeTo: this.hostEl,
    });
    this.hostEl.innerHTML = '';
    this.hostEl.appendChild(this.app.canvas);

    this.fieldLayer = new Container();
    this.agentLayer = new Container();
    this.app.stage.addChild(this.fieldLayer);
    this.app.stage.addChild(this.agentLayer);

    this.sheepTexture = await Assets.load(sheepUrl);
    this.dogTexture = await Assets.load(dogUrl);
    this._ready = true;
    this._drawField();
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

  _scale() {
    const w = this.app.renderer.width;
    const h = this.app.renderer.height;
    return {
      sx: w / this.world.width,
      sy: h / this.world.height,
      w,
      h,
    };
  }

  _drawField() {
    this.fieldLayer.removeChildren();
    const { sx, sy, w, h } = this._scale();
    const g = new Graphics();

    g.rect(0, 0, w, h);
    g.fill({ color: 0x090d16 });

    g.setStrokeStyle({ width: 1, color: 0xffffff, alpha: 0.05 });
    const step = 15 * sx;
    for (let x = 0; x <= w; x += step) {
      g.moveTo(x, 0);
      g.lineTo(x, h);
    }
    for (let y = 0; y <= h; y += step) {
      g.moveTo(0, y);
      g.lineTo(w, y);
    }
    g.stroke();

    for (const obs of this.world.obstacles) {
      const [x0, y0] = obs.min_corner;
      const [x1, y1] = obs.max_corner;
      g.rect(x0 * sx, y0 * sy, (x1 - x0) * sx, (y1 - y0) * sy);
      g.fill({ color: 0x334155, alpha: 0.85 });
    }

    if (this.world.goal_center && this.world.goal_radius != null) {
      const [gx, gy] = this.world.goal_center;
      const gr = this.world.goal_radius * sx;
      g.circle(gx * sx, gy * sy, gr);
      g.fill({ color: 0x22c55e, alpha: 0.15 });
      g.setStrokeStyle({ width: 2, color: 0x22c55e, alpha: 0.9 });
      g.circle(gx * sx, gy * sy, gr);
      g.stroke();
    }

    this.fieldLayer.addChild(g);
  }

  _ensureSprites(count, pool, texture, size) {
    while (pool.length < count) {
      const sprite = new Sprite(texture);
      sprite.anchor.set(0.5);
      sprite.width = size;
      sprite.height = size;
      this.agentLayer.addChild(sprite);
      pool.push(sprite);
    }
    for (let i = 0; i < pool.length; i += 1) {
      pool[i].visible = i < count;
    }
  }

  render(frame) {
    if (!this._ready || !frame) return;
    if (frame.world) this.setWorld(frame.world);

    const { sx, sy } = this._scale();
    const sheep = frame.sheep_positions || [];
    const dogs = frame.shepherd_positions || [];
    const sheepHeadings = frame.sheep_headings || [];
    const dogHeadings = frame.shepherd_headings || [];

    this._ensureSprites(sheep.length, this.sheepSprites, this.sheepTexture, 18);
    this._ensureSprites(dogs.length, this.dogSprites, this.dogTexture, 22);

    sheep.forEach((pos, i) => {
      const sprite = this.sheepSprites[i];
      sprite.x = pos[0] * sx;
      sprite.y = pos[1] * sy;
      if (sheepHeadings[i] != null) sprite.rotation = sheepHeadings[i];
    });

    dogs.forEach((pos, i) => {
      const sprite = this.dogSprites[i];
      sprite.x = pos[0] * sx;
      sprite.y = pos[1] * sy;
      if (dogHeadings[i] != null) sprite.rotation = dogHeadings[i];
    });
  }

  destroy() {
    if (this.app) {
      this.app.destroy(true);
      this.app = null;
    }
    this._ready = false;
  }
}
