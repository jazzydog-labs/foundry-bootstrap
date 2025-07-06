from orchestrate.main import BootstrapOrchestrator

def test_fallback_called(monkeypatch, tmp_path):
    config = tmp_path
    (config / 'packages.yaml').write_text('packages:\n  - just\n')
    orch = BootstrapOrchestrator(config)
    monkeypatch.setattr(orch, 'apt_package_exists', lambda pkg: False)
    calls = []
    def fake_run(cmd, desc, env=None):
        calls.append((cmd, desc))
        return True
    monkeypatch.setattr(orch, 'run_command', fake_run)
    assert orch.install_system_packages() is True
    assert any('fallback install just' in c[1] for c in calls)
