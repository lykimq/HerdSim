import { Application, Container, Graphics, Sprite, Text } from 'pixi.js';
import { loadIconTextures } from './iconTextures.js';
import { drawField } from './drawField.js';
import {
  appendTrailPositions,
  ASSIGNMENT_COLLECT_COLOR,
  ASSIGNMENT_DRIVE_COLOR,
  trailColor,
  trailsFromFrames,
} from './herderTrails.js';
import { parseOverlayColor, GCM_GOAL_COLOR, sheepCentroid } from '../utils/displayOverlays.js';
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
    this.trailLayer = null;
    this.agentLayer = null;
    this.assignmentLayer = null;
    this.gcmGoalLayer = null;
    this.hudLayer = null;
    this.textures = { sheep: null, dog: null, shepherd: null, goal: null, pen: null };
    this.herderKind = 'dog';
    this.trailVisible = true;
    this.gcmGoalVisible = true;
    this.assignmentModeVisible = {};
    this.assignmentModeColors = {};
    this.trailPoints = [];
    this._lastFrame = null;
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
        preference: 'webgl',
      });
      this.hostEl.innerHTML = '';
      this.hostEl.appendChild(this.app.canvas);

      this.fieldLayer = new Container();
      this.trailLayer = new Container();
      this.agentLayer = new Container();
      this.assignmentLayer = new Container();
      this.gcmGoalLayer = new Container();
      this.hudLayer = new Container();
      this.app.stage.addChild(this.fieldLayer);
      this.app.stage.addChild(this.trailLayer);
      this.app.stage.addChild(this.agentLayer);
      this.app.stage.addChild(this.assignmentLayer);
      this.app.stage.addChild(this.gcmGoalLayer);
      this.app.stage.addChild(this.hudLayer);

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

  setTrailVisible(visible) {
    this.trailVisible = Boolean(visible);
    this._drawTrails();
  }

  setGcmGoalVisible(visible) {
    this.gcmGoalVisible = Boolean(visible);
    this._redrawGcmGoal();
  }

  setAssignmentModes(modes) {
    const nextVisible = {};
    const nextColors = {};
    (modes || []).forEach((mode) => {
      const id = mode?.id;
      if (!id) return;
      nextVisible[id] =
        this.assignmentModeVisible[id] !== undefined
          ? this.assignmentModeVisible[id]
          : true;
      nextColors[id] = parseOverlayColor(
        mode.color,
        id === 'collect' ? ASSIGNMENT_COLLECT_COLOR : ASSIGNMENT_DRIVE_COLOR,
      );
    });
    this.assignmentModeVisible = nextVisible;
    this.assignmentModeColors = nextColors;
    this._redrawAssignment();
  }

  setAssignmentModeVisible(modeId, visible) {
    if (!modeId) return;
    this.assignmentModeVisible[modeId] = Boolean(visible);
    this._redrawAssignment();
  }

  _redrawAssignment() {
    if (this._lastFrame) this._drawAssignmentOverlay(this._lastFrame);
  }

  _redrawGcmGoal() {
    if (this._lastFrame) this._drawGcmGoalOverlay(this._lastFrame);
    else if (this.gcmGoalLayer) this.gcmGoalLayer.removeChildren();
  }

  clearTrails() {
    this.trailPoints = [];
    this._drawTrails();
  }

  setTrailsFromFrames(frames) {
    this.trailPoints = trailsFromFrames(frames);
    this._drawTrails();
  }

  _herderTexture() {
    return this.herderKind === 'human' ? this.textures.shepherd : this.textures.dog;
  }

  _scale() {
    const w = this.app.renderer.width;
    const h = this.app.renderer.height;
    const pad = 18;
    const s = Math.min(
      (w - pad * 1.35) / this.world.width,
      (h - pad * 1.35) / this.world.height,
    );
    const offsetX = pad + (w - pad * 1.35 - this.world.width * s) / 2;
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
    this._drawTrails();
    this._redrawGcmGoal();
  }

  /**
   * @param {object} frame
   * @param {{ recordTrail?: boolean }} [options]
   */
  render(frame, options = {}) {
    if (!this._ready || !frame) return;
    const recordTrail = options.recordTrail !== false;
    this._lastFrame = frame;
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

    if (recordTrail) {
      this.trailPoints = appendTrailPositions(this.trailPoints, dogs);
    }
    this._drawTrails();
    this._drawAssignmentOverlay(frame);
    this._drawGcmGoalOverlay(frame);
  }

  _drawTrails() {
    if (!this.trailLayer) return;
    this.trailLayer.removeChildren();
    if (!this.trailVisible || !this.trailPoints.length) return;

    const g = new Graphics();
    this.trailPoints.forEach((poly, idx) => {
      if (!poly || poly.length < 2) return;
      const [x0, y0] = this._toScreen(poly[0][0], poly[0][1]);
      g.moveTo(x0, y0);
      for (let i = 1; i < poly.length; i += 1) {
        const [x, y] = this._toScreen(poly[i][0], poly[i][1]);
        g.lineTo(x, y);
      }
      g.stroke({
        width: 1.4,
        color: trailColor(idx),
        alpha: 0.55,
      });
    });
    this.trailLayer.addChild(g);
  }

  _drawAssignmentOverlay(frame) {
    this.assignmentLayer.removeChildren();
    const lines = frame?.metadata?.assignment_lines;
    if (!Array.isArray(lines) || lines.length === 0) return;

    const g = new Graphics();
    lines.forEach((line) => {
      const from = line?.from;
      const to = line?.to;
      if (!Array.isArray(from) || !Array.isArray(to)) return;
      const mode = String(line.mode || 'target');
      if (this.assignmentModeVisible[mode] === false) return;
      // If modes are declared and this mode is unknown, hide it.
      if (
        Object.keys(this.assignmentModeVisible).length > 0 &&
        this.assignmentModeVisible[mode] === undefined
      ) {
        return;
      }
      const [x1, y1] = this._toScreen(from[0], from[1]);
      const [x2, y2] = this._toScreen(to[0], to[1]);
      const color =
        this.assignmentModeColors[mode] ??
        (mode === 'collect' ? ASSIGNMENT_COLLECT_COLOR : ASSIGNMENT_DRIVE_COLOR);
      g.moveTo(x1, y1);
      g.lineTo(x2, y2);
      g.stroke({
        width: mode === 'collect' ? 1.6 : 1.1,
        color,
        alpha: mode === 'collect' ? 0.85 : 0.55,
      });
    });
    this.assignmentLayer.addChild(g);
  }

  _drawGcmGoalOverlay(frame) {
    if (!this.gcmGoalLayer) return;
    this.gcmGoalLayer.removeChildren();
    if (!this.gcmGoalVisible || !frame) return;

    const gcm = sheepCentroid(frame.sheep_positions);
    const goal = frame.world?.goal_center ?? this.world.goal_center;
    if (!gcm || !Array.isArray(goal) || goal.length < 2) return;

    const [x1, y1] = this._toScreen(gcm[0], gcm[1]);
    const [x2, y2] = this._toScreen(Number(goal[0]), Number(goal[1]));
    const color = parseOverlayColor(GCM_GOAL_COLOR, 0xc084fc);
    const { s } = this._scale();
    const markerR = Math.max(3.5, 2.2 * s);

    const g = new Graphics();
    g.moveTo(x1, y1);
    g.lineTo(x2, y2);
    g.stroke({ width: 1.5, color, alpha: 0.75 });
    g.circle(x1, y1, markerR);
    g.stroke({ width: 1.4, color, alpha: 0.95 });
    g.circle(x1, y1, Math.max(1.2, markerR * 0.35));
    g.fill({ color, alpha: 0.9 });
    this.gcmGoalLayer.addChild(g);
  }

  destroy() {
    if (this.app) {
      this.app.destroy(
        { removeView: true },
        { children: true, texture: false, textureSource: false },
      );
      this.app = null;
    }
    this._ready = false;
    log.debug('pixi', 'Renderer destroyed');
  }

  /** Force a layout pass after the host was display:none (tab keep-alive). */
  resize() {
    if (!this.app?.renderer || !this.hostEl) return;
    const w = this.hostEl.clientWidth;
    const h = this.hostEl.clientHeight;
    if (w <= 0 || h <= 0) return;
    this.app.renderer.resize(w, h);
    if (this._ready) this._drawField();
  }
}
