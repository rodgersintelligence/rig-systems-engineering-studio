import { Text } from '@react-three/drei';
import { ALTITUDE_ORDER, DIAMOND_ORDER, MODE_ORDER, STEP_ORDER } from '../types/lattice';

const AXIS_OFFSET = -1.2;
const LABEL_COLOR = '#94a3b8';
const TITLE_COLOR = '#e2e8f0';

export function Axes() {
  return (
    <>
      {/* X-axis: Altitude (7) */}
      {ALTITUDE_ORDER.map((alt, i) => (
        <Text
          key={`x-${alt}`}
          position={[i, AXIS_OFFSET, AXIS_OFFSET]}
          fontSize={0.35}
          color={LABEL_COLOR}
          anchorX="center"
          anchorY="top"
        >
          {alt}
        </Text>
      ))}
      <Text
        position={[3, AXIS_OFFSET - 1.4, AXIS_OFFSET]}
        fontSize={0.45}
        color={TITLE_COLOR}
        anchorX="center"
      >
        X — Altitude (7)
      </Text>

      {/* Y-axis: Diamond × IQRSQPI (21) */}
      {DIAMOND_ORDER.flatMap((d) =>
        STEP_ORDER.map((s, j) => {
          const di = DIAMOND_ORDER.indexOf(d);
          return (
            <Text
              key={`y-${d}.${s}`}
              position={[AXIS_OFFSET, di * 7 + j, AXIS_OFFSET]}
              fontSize={0.22}
              color={LABEL_COLOR}
              anchorX="right"
              anchorY="middle"
            >
              {`${d}.${s}`}
            </Text>
          );
        })
      )}
      <Text
        position={[AXIS_OFFSET - 2.2, 10, AXIS_OFFSET]}
        fontSize={0.45}
        color={TITLE_COLOR}
        rotation={[0, 0, Math.PI / 2]}
        anchorX="center"
      >
        Y — Diamond × IQRSQPI (21)
      </Text>

      {/* Z-axis: Mode (4) */}
      {MODE_ORDER.map((m, i) => (
        <Text
          key={`z-${m}`}
          position={[AXIS_OFFSET, AXIS_OFFSET, i]}
          fontSize={0.32}
          color={LABEL_COLOR}
          anchorX="right"
          anchorY="middle"
          rotation={[0, -Math.PI / 2, 0]}
        >
          {m}
        </Text>
      ))}
      <Text
        position={[AXIS_OFFSET, AXIS_OFFSET - 1.4, 1.5]}
        fontSize={0.45}
        color={TITLE_COLOR}
        anchorX="center"
      >
        Z — Mode (4)
      </Text>
    </>
  );
}
