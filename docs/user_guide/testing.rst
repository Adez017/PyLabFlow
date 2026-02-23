Testing Strategy
================

PyLabFlow uses a two-layer test strategy:

- Unit tests for deterministic logic (hashing, configuration parsing, validation helpers).
- Integration tests for filesystem + SQLite flow (lab setup, logs, pipeline lifecycle).

Pytest Structure
----------------

Recommended structure:

- ``tests/conftest.py``: shared fixtures for temporary project environments.
- ``tests/unit/``: fast, isolated unit tests with no external side effects.
- ``tests/integration/``: real file/database flow tests built on temp directories.

Current examples:

- ``tests/unit/test_utils_core.py``
- ``tests/integration/test_lab_setup.py``
- ``tests/integration/test_pipeline_lifecycle.py``

Running Tests Locally
---------------------

Run all tests:

.. code-block:: bash

   pytest

Run only unit tests:

.. code-block:: bash

   pytest tests/unit

Run only integration tests:

.. code-block:: bash

   pytest -m integration

CI Compatibility
----------------

The test suite is CI-friendly because it:

- Uses temporary directories via pytest fixtures.
- Avoids network dependencies.
- Keeps unit tests independent from integration state.
- Uses standard pytest markers so CI can split jobs.

Typical CI commands:

.. code-block:: bash

   pip install -e .
   pip install pytest
   pytest tests/unit
   pytest -m integration

Test Authoring Guidelines
-------------------------

- Keep unit tests pure and fast.
- Use ``tmp_path`` / ``tmp_path_factory`` for file writes.
- Mark cross-module/database tests with ``@pytest.mark.integration``.
- Prefer explicit assertions over print-based verification.
- Avoid relying on execution order between tests.
