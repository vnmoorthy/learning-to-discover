# Phoenixastar: talk track (3 minutes, spoken style)

Say this the way you would explain it to a friend at the table, not like reading. About 450 words, roughly 3 minutes.
Live counters keep moving, so numbers are said as floors ("over seventeen hundred"). Sponsors named in the script:
Lambda, Modal, past.dev, Exa, OpenAI (GPT-6 Astra), Anthropic (Claude Fable 5.2), Tinker and Devin.

**How to record (for the demo video):** one take, landscape 1920x1080, face centred with some headroom, quiet room,
look at the lens. **Pause for one full second between sections** (that is where the video cuts). Save the file as
`video/me/take.mov` (or `.mp4`). I transcribe it with timestamps, cut the screen recording of each section to your
timing, and place you as picture-in-picture over your own voice. Small wording changes are fine; keep the first few
words of each section, because that is how the video finds the cuts.

---

## 1. Hook (0:00-0:15) · screen: banner, then Mission Control hero

> So here's a question I wanted to answer: can an AI run a research lab by itself, and can you actually trust what it
> tells you? I built Phoenixastar to find out. It works on open problems in math and physics, and nothing counts until
> an exact verifier checks it.

## 2. The loop and the sponsors (0:15-0:50) · screen: Mission Control, the loop stepper, then the compute map

> Here's how it works. Every three minutes the loop wakes up and looks at everything that's running: eight A100s on
> Lambda, 124 CPU cores, and up to 140 containers on Modal. First it re-checks every result with the official
> verifiers. It remembers what it learned with past.dev, and it pulls in papers with Exa. Then GPT-6 Astra proposes the
> next experiment, and it has to make a prediction we can check later. Claude Fable 5.2 reviews every proposal and can
> veto it. That's over seventeen hundred decisions so far, and every single one is logged.

## 3. Honest math (0:50-1:05) · screen: Decisions page, a refuted prediction; then No-three-in-line 75

> And those predictions really do get checked. Here it expected sixteen collinear triples, it got seventeen, and it
> marked itself wrong. We haven't beaten an EinsteinArena record yet, and the dashboard shows you exactly how far off
> we are.

## 4. Event Horizon (1:05-1:45) · screen: black hole, drag it, zoom to the photon ring, toggle Lensing off and on

> Now, the same loop does physics too. This black hole isn't a video. Your browser is ray-tracing light through curved
> spacetime, live. Watch what happens when I turn lensing off... that's what gravity is doing to the picture. Behind it
> is Event Horizon, a study of how information gets out of an evaporating black hole. We reproduced the Page curve up
> to 24 qubits on an A100, and this afternoon it added entanglement spectra, recovery fidelity and error-correcting
> codes. A separate verifier re-derives the key numbers, and it actually caught one of our claims that was wrong.

## 5. STARFORGE (1:45-2:10) · screen: STARFORGE page, the neutron-star cutaway, then the twin-star figure

> Starforge goes after neutron stars: what is matter actually made of in there? It solves Einstein's equations for the
> star, and a second, independent solver agrees to about one part in a million. You can cut one open right here. It
> found twin stars: same mass, but one is twelve kilometres across and the other is nine. And when its Bayesian
> inference didn't converge in time, it just said so. No posterior. I really like that.

## 6. Three-body (2:10-2:22) · screen: Physics, the interactive three-body orbits

> On the three-body problem, the GPU search found seventeen periodic orbits in sixteen families that aren't among the
> 2,060 catalogued ones we checked. We call them candidates, not discoveries.

## 7. It learns (2:22-2:45) · screen: Self-improvement, the Tinker curve; then Memory benchmark

> The lab also gets better on its own. Tinker fine-tunes an open model with the verifier as the reward, and valid
> answers went from zero to fifty percent. Devin writes new search tools, and they run sealed in Modal sandboxes before
> we trust them. And we benchmarked our own memory honestly: plain markdown still beats it.

## 8. Close (2:45-3:00) · screen: banner, replay link

> So, no breakthroughs claimed. Just a lab that does the work, checks itself, and shows you everything. That's
> Phoenixastar.

---

## Live finals click path (if presenting live instead of the video)

1. `vnmoorthy.github.io/phoenixastar` or the live lab, Mission Control: point at the loop stepper and the counters.
2. Decisions: filter "critic", open a refuted prediction.
3. Home card black hole: drag, scroll to zoom, toggle Lensing.
4. Problems, EVENT HORIZON: Interactive tab, then one figure and its verification.
5. Problems, STARFORGE: the neutron-star cutaway (switch to the maximum-mass star), then the twin-star figure.
6. Physics: three-body orbits, drag to rotate.
7. Self-improvement: Tinker curve. Close on the banner.

**Backup lines if asked:** "Have you beaten a record?" No, and the dashboard shows the exact gap for each one. "Is the
black hole real?" It's a physically based simulation of a Schwarzschild black hole; the gas texture is procedural.
"What's new?" Every claim is classified: most results are reproductions or new computational explorations (levels
1-3); the three-body orbits and a few hypotheses are candidates that need expert review.
