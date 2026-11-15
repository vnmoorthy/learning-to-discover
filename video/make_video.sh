#!/bin/zsh
# One command to rebuild the demo video end to end.
#   ./make_video.sh            fresh numbers + TTS, re-record every shot, assemble
#   KEEP_AUDIO=1 ./make_video.sh   keep the existing narration (no TTS call), re-record + assemble
#   ./make_video.sh s2_loop s8_gallery   re-record only those shots (keeps audio), then assemble
# Shots: s2_loop s3_compute s4_problem s5a_dec211 s5b_dec219 s5c_dec191 s6_memory s7_learning s8_gallery
set -e
cd "$(dirname "$0")"
if [[ $# -eq 0 && -z "$KEEP_AUDIO" ]]; then python3 narrate.py; python3 prep_audio.py; fi
python3 -u record.py "$@"
python3 assemble.py
python3 write_script_md.py
