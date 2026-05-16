import { Text } from '@react-three/drei';
import { ALTITUDE_ORDER, CONFIDENCE_ORDER, DIAMOND_ORDER, STEP_ORDER } from '../types/lattice';

const AXIS_OFFSET = -1.2;
const LABEL_COLOR = '#94a3b8';
const TITLE_COLOR = '#e2e8f0';

export function Axes() {
  return (
    <>
      {/* X-axis: Altitude */}
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
        X — Altitude
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
        position={[AXIS_OFFSET - 2.0, 10, AXIS_OFFSET]}
        fontSize={0.45}
        color={TITLE_COLOR}
        rotation={[0, 0, Math.PI / 2]}
        anchorX="center"
      >
        Y — Triple Diamond × IQRSQPI
      </Text>

      {/* Z-axis: Confidence × IQRSQPI (21) */}
      {CONFIDENCE_ORDER.flatMap((c) =>
        STEP_ORDER.map((s, j) => {
          const ci = CONFIDENCE_ORDER.indexOf(c);
          return (
            <Text
              key={`z-${c}.${s}`}
              position={[AXIS_OFFSET, AXIS_OFFSET, ci * 7 + j]}
              fontSize={0.22}
              color={LABEL_COLOR}
              anchorX="right"
              anchorY="middle"
              rotation={[0, -Math.PI / 2, 0]}
            >
              {`${c.replace('ADJ_', '')}.${s}`}
            </Text>
          );
        })
      )}
      <Text
        position={[AXIS_OFFSET, AXIS_OFFSET - 1.4, 10]}
        fontSize={0.45}
        color={TITLE_COLOR}
        anchorX="center"
      >
        Z — BMS Confidence × IQRSQPI
      </Text>
    </>
  );
}
