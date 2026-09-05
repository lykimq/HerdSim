/**
 * Icon helpers for HerdSim.
 *
 * Canvas / animals / field objects: Game Icons via @iconify-json/game-icons (CC BY 3.0).
 * UI chrome (playback, export): Lucide (ISC).
 *
 * Attribution: Icons made by Delapouite, Lorc & contributors. Available on https://game-icons.net
 */

import gameIconSet from './game-icons-subset.json';
import { getIconData, iconToSVG } from '@iconify/utils';
import {
  Play,
  Pause,
  RotateCcw,
  SkipForward,
  Download,
  Square,
  Settings,
  SlidersHorizontal,
  ChartColumn,
  Clock,
  Eye,
  EyeOff,
  Info,
  CircleHelp,
  Plus,
  Minus,
  Maximize,
  ZoomIn,
  ZoomOut,
  Grid3x3,
} from 'lucide';

export const ICON_COLORS = {
  sheep: '#FFFFFF',
  dog: '#FBBF24',
  shepherd: '#76A04D',
  goal: '#D13438',
  pen: '#8E644B',
  waypoint: '#54B948',
  ui: 'currentColor',
};

const GAME_ICON_NAMES = {
  sheep: 'sheep',
  dog: 'sitting-dog',
  dogStanding: 'jumping-dog',
  shepherd: 'farmer',
  goal: 'archery-target',
  pen: 'wooden-fence',
  gate: 'stakes-fence',
  waypoint: 'golf-flag',
};

const LUCIDE_NODES = {
  play: Play,
  pause: Pause,
  reset: RotateCcw,
  step: SkipForward,
  stop: Square,
  export: Download,
  release: Play,
  settings: Settings,
  parameters: SlidersHorizontal,
  charts: ChartColumn,
  time: Clock,
  visibility: Eye,
  hide: EyeOff,
  info: Info,
  help: CircleHelp,
  add: Plus,
  remove: Minus,
  fullscreen: Maximize,
  zoomIn: ZoomIn,
  zoomOut: ZoomOut,
  grid: Grid3x3,
};

function attrsToString(attrs) {
  return Object.entries(attrs)
    .map(([key, value]) => `${key}="${String(value).replace(/"/g, '&quot;')}"`)
    .join(' ');
}

/** Build a data-URL SVG from a Game Icons glyph. */
export function gameIconDataUrl(name, color = '#ffffff', size = 128) {
  const data = getIconData(gameIconSet, name);
  if (!data) {
    throw new Error(`Unknown game-icons glyph: ${name}`);
  }
  const rendered = iconToSVG(data, { width: size, height: size });
  const body = rendered.body.replace(/currentColor/g, color);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" ${attrsToString(rendered.attributes)}>${body}</svg>`;
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

function lucideToSvg(iconNode, className = 'icon', size = 18) {
  const children = iconNode
    .map(([tag, attrs]) => `<${tag} ${attrsToString(attrs)} />`)
    .join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="${className}" aria-hidden="true">${children}</svg>`;
}

/** Texture URLs for Pixi (Game Icons, recolored for the dark field). */
export const icons = {
  sheep: gameIconDataUrl(GAME_ICON_NAMES.sheep, ICON_COLORS.sheep, 128),
  dog: gameIconDataUrl(GAME_ICON_NAMES.dog, ICON_COLORS.dog, 128),
  shepherd: gameIconDataUrl(GAME_ICON_NAMES.shepherd, ICON_COLORS.shepherd, 128),
  goal: gameIconDataUrl(GAME_ICON_NAMES.goal, ICON_COLORS.goal, 128),
  pen: gameIconDataUrl(GAME_ICON_NAMES.pen, ICON_COLORS.pen, 128),
  gate: gameIconDataUrl(GAME_ICON_NAMES.gate, ICON_COLORS.pen, 128),
  waypoint: gameIconDataUrl(GAME_ICON_NAMES.waypoint, ICON_COLORS.waypoint, 128),
};

/** Resolve which Game Icon key to use for a herding agent. */
export function herderIconName(herderKind) {
  return herderKind === 'human' ? 'shepherd' : 'dog';
}

export function herderColor(herderKind) {
  return herderKind === 'human' ? ICON_COLORS.shepherd : ICON_COLORS.dog;
}

/**
 * Inline icon HTML for buttons/labels.
 * Animals/objects use Game Icons; playback/UI use Lucide.
 */
export function iconImg(name, className = 'icon') {
  if (GAME_ICON_NAMES[name]) {
    const color =
      name === 'sheep'
        ? ICON_COLORS.sheep
        : name === 'dog' || name === 'dogStanding'
          ? ICON_COLORS.dog
          : name === 'shepherd'
            ? ICON_COLORS.shepherd
            : name === 'goal'
              ? ICON_COLORS.goal
              : name === 'waypoint'
                ? ICON_COLORS.waypoint
                : ICON_COLORS.pen;
    const src = gameIconDataUrl(GAME_ICON_NAMES[name], color, 64);
    return `<img class="${className}" src="${src}" alt="" aria-hidden="true" />`;
  }
  const node = LUCIDE_NODES[name];
  if (!node) return '';
  return lucideToSvg(node, className);
}

export const GAME_ICONS_ATTRIBUTION =
  'Simulation icons by Delapouite, Lorc & contributors (game-icons.net), CC BY 3.0.';
