"""Root launcher for the food-prep Streamlit UI.

Run with:  streamlit run app.py

This thin shim exists so `streamlit run app.py` works from the project root
without typing the package path. The real app is
``src/foodprep/ui/streamlit_app.py``.

We import and call ``main()`` rather than ``from ... import *`` so the app body
runs on every Streamlit rerun (widget interaction / new session). With
``import *`` the module body runs only once per process — Python caches it in
``sys.modules`` — so every session after the first saw an empty canvas.
Calling ``main()`` here re-executes the rendering on each rerun, which is how
Streamlit is meant to be driven.
"""

from foodprep.ui.streamlit_app import main

main()