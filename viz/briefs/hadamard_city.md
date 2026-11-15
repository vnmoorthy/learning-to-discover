# Brief: "Hadamard City" for the maximal-determinant problem (order 51)

Project: "Phoenixastar", an AI lab that gets better at discovering mathematics by doing it. The
current record for the largest determinant of a 51x51 matrix with entries +1/-1 has log10|det| = 43.3375.
This image turns that exact record matrix into an extruded city / terrain at night. It must look stunning,
premium and clean.

## Data (JSON at --data; real record matrix, do not invent anything)
```
{ "n": 51, "matrix": [[1, -1, ...], ...],   # 51 rows x 51 cols, entries exactly 1 or -1
  "log10_det": 43.33745596194037, "holder": "kgrey" }
```

## Scene (art direction)
- Cell (i, j) (row i, column j) is a block on a 51x51 grid (spacing 1.0, block footprint ~0.86 x 0.86,
  centered on the origin, row 0 at the back).
- Height comes from the data only: +1 cells are towers, -1 cells are low plinths. To give it a city/terrain
  rhythm, modulate height by the local agreement of the matrix: s(i,j) = mean of the entries in the 5x5
  neighbourhood (clipped at the borders). Use exactly h_plus = 0.9 + 2.6 * (s + 1) / 2 for +1 cells and
  h_minus = 0.12 + 0.2 * (s + 1) / 2 for -1 cells (purely data-derived; no random or decorative height terms).
- Materials: dark architectural glass/graphite towers (#101318, roughness ~0.3) with an emissive cyan #3DF5FF
  cap / top edge on +1 towers (thin glowing roof slab), and the -1 plinths carrying a dim warm amber #FFB547
  glow on their tops (lower strength than the cyan) so the sign pattern reads from above like city lights.
- Dark studio environment (#07080B world, low strength), a dark reflective ground plane under the city, slight
  haze is optional (skip volumetrics if slow).
- Lighting: cool soft area light from high back-left as rim; emissive caps do the rest.
- Camera: aerial 3/4 view at ~35-45 degrees elevation from a corner, lens ~50-85 mm, the whole 51x51 city in
  frame with some breathing room but filling most of the frame. Tilt-shift / miniature feel through depth of
  field: focus on the city center, fstop ~1.4-2.0 so front and back edges blur.
- Post: compositor Glare 'Bloom', AgX view transform with a punchy look. No text.

## Script contract (args after `--`)
- `--data PATH` (hadamard JSON), `--out PATH` (absolute .png)
- `--res WxH` (default 1920x1080), `--samples N` (EEVEE taa_render_samples, default 64)
- Build all 2601 blocks as ONE mesh (plus one mesh for the emissive caps), not 2601 objects.
