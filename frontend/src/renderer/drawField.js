import { Graphics } from 'pixi.js';
import { log } from '../utils/logger.js';

/** Major grid spacing in world units (simulation meters / paper units). */
const GRID_MAJOR = 25;
/** Minor grid spacing in world units. */
const GRID_MINOR = 5;
/** Axis label step (keep sparse for performance). */
const LABEL_STEP = 50;

/**
 * Draw the pasture field, grid, obstacles, and goal into the renderer layers.
 * @param {object} ctx PixiRenderer-like context with layers, world, and helpers.
 */
export function drawField(ctx) {
  if (!ctx._ready || !ctx.app?.renderer) return;
  ctx.fieldLayer.removeChildren();
  ctx.overlayLayer.removeChildren();
  const { s, offsetX, offsetY, pad, w, h } = ctx._scale();
  if (w < 40 || h < 40) {
    log.debug('pixi', 'Skip field draw; canvas not laid out yet', { w, h });
    return;
  }
  const fieldW = ctx.world.width * s;
  const fieldH = ctx.world.height * s;
  const g = new Graphics();

  g.rect(0, 0, ctx.app.renderer.width, ctx.app.renderer.height);
  g.fill({ color: 0x090d16 });

  // Pasture / arena fill
  g.rect(offsetX, offsetY, fieldW, fieldH);
  g.fill({ color: 0x102018 });

  // Minor grid
  g.setStrokeStyle({ width: 1, color: 0xffffff, alpha: 0.04 });
  for (let x = 0; x <= ctx.world.width + 0.01; x += GRID_MINOR) {
    if (x % GRID_MAJOR === 0) continue;
    const [sx] = ctx._toScreen(x, 0);
    g.moveTo(sx, offsetY);
    g.lineTo(sx, offsetY + fieldH);
  }
  for (let y = 0; y <= ctx.world.height + 0.01; y += GRID_MINOR) {
    if (y % GRID_MAJOR === 0) continue;
    const [, sy] = ctx._toScreen(0, y);
    g.moveTo(offsetX, sy);
    g.lineTo(offsetX + fieldW, sy);
  }
  g.stroke();

  // Major grid (world units)
  g.setStrokeStyle({ width: 1, color: 0xffffff, alpha: 0.12 });
  for (let x = 0; x <= ctx.world.width + 0.01; x += GRID_MAJOR) {
    const [sx] = ctx._toScreen(x, 0);
    g.moveTo(sx, offsetY);
    g.lineTo(sx, offsetY + fieldH);
  }
  for (let y = 0; y <= ctx.world.height + 0.01; y += GRID_MAJOR) {
    const [, sy] = ctx._toScreen(0, y);
    g.moveTo(offsetX, sy);
    g.lineTo(offsetX + fieldW, sy);
  }
  g.stroke();

  // Field border
  g.setStrokeStyle({ width: 2, color: 0xcbd5e1, alpha: 0.55 });
  g.rect(offsetX, offsetY, fieldW, fieldH);
  g.stroke();

  ctx.fieldLayer.addChild(g);

  // Axis tick labels (world units) -- sparse for readability/perf
  for (let x = 0; x <= ctx.world.width + 0.01; x += LABEL_STEP) {
    const [sx] = ctx._toScreen(x, 0);
    ctx.overlayLayer.addChild(
      ctx._makeLabel(String(x), sx, offsetY + fieldH + 10, { size: 9, ay: 0 }),
    );
  }
  for (let y = 0; y <= ctx.world.height + 0.01; y += LABEL_STEP) {
    const [, sy] = ctx._toScreen(0, y);
    ctx.overlayLayer.addChild(
      ctx._makeLabel(String(y), offsetX - 8, sy, { size: 9, ax: 1 }),
    );
  }
  ctx.overlayLayer.addChild(
    ctx._makeLabel('x', offsetX + fieldW / 2, offsetY + fieldH + 20, {
      size: 10,
      fill: 0x64748b,
    }),
  );
  ctx.overlayLayer.addChild(
    ctx._makeLabel('y', Math.max(10, offsetX - pad + 4), offsetY + fieldH / 2, {
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
  ctx.overlayLayer.addChild(bar);
  ctx.overlayLayer.addChild(
    ctx._makeLabel(`${barWorld} units`, barX + barPx / 2, barY + 10, {
      size: 9,
      fill: 0xe2e8f0,
    }),
  );

  for (const obs of ctx.world.obstacles) {
    const [x0, y0] = obs.min_corner;
    const [x1, y1] = obs.max_corner;
    const [sx0, sy0] = ctx._toScreen(x0, y1);
    const [sx1, sy1] = ctx._toScreen(x1, y0);
    const ow = Math.abs(sx1 - sx0);
    const oh = Math.abs(sy1 - sy0);
    const cx = (sx0 + sx1) / 2;
    const cy = (sy0 + sy1) / 2;
    if (ctx.textures.pen) {
      const fence = ctx._placeSprite(ctx.textures.pen, cx, cy, Math.min(ow, oh));
      fence.width = ow;
      fence.height = oh;
      ctx.fieldLayer.addChild(fence);
    } else {
      const box = new Graphics();
      box.rect(Math.min(sx0, sx1), Math.min(sy0, sy1), ow, oh);
      box.fill({ color: 0x8e644b, alpha: 0.9 });
      ctx.fieldLayer.addChild(box);
    }
  }

  if (ctx.world.goal_center && ctx.world.goal_radius != null) {
    const [gx, gy] = ctx.world.goal_center;
    const [sx, sy] = ctx._toScreen(gx, gy);
    const gr = ctx.world.goal_radius * s;
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
    ctx.fieldLayer.addChild(ring);
    if (ctx.textures.goal) {
      const marker = ctx._placeSprite(
        ctx.textures.goal,
        sx,
        sy,
        Math.max(14, Math.min(gr * 0.55, 32)),
      );
      ctx.fieldLayer.addChild(marker);
    }
    ctx.overlayLayer.addChild(
      ctx._makeLabel('GOAL', sx, sy - gr - 8, {
        size: 11,
        fill: 0xfca5a5,
        bold: true,
      }),
    );
  }
}
