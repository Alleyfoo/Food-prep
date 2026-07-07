"""Root launcher for the food-prep Streamlit UI.

Run with:  streamlit run app.py

This thin shim exists so `streamlit run app.py` works from the project root
without typing the package path. The real app is
``src/foodprep/ui/streamlit_app.py``.
"""

from foodprep.ui.streamlit_app import *  # noqa: F401,F403  (executes the app)