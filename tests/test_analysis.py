"""
CSC Latin America 2026 - Python Analysis Tests
Tests for ROOT/Python integration
"""

import pytest
import math


def test_import_root():
    """Test that ROOT can be imported"""
    try:
        import ROOT
        assert ROOT.gROOT is not None
    except ImportError:
        pytest.skip("ROOT not available")


def test_root_version():
    """Test ROOT version is reasonable"""
    try:
        import ROOT
        version = ROOT.gROOT.GetVersion()
        major = int(version.split('.')[0])
        assert major >= 6, f"Expected ROOT 6+, got {version}"
    except ImportError:
        pytest.skip("ROOT not available")


def test_create_histogram():
    """Test creating a simple histogram"""
    try:
        import ROOT
        h = ROOT.TH1F("test_hist", "Test;x;counts", 100, 0, 1)
        assert h.GetNbinsX() == 100
        h.Fill(0.5)
        assert h.GetEntries() == 1
    except ImportError:
        pytest.skip("ROOT not available")


def test_lorentz_vector():
    """Test TLorentzVector operations"""
    try:
        import ROOT
        
        # Create two particles
        p1 = ROOT.TLorentzVector()
        p1.SetPxPyPzE(10, 0, 30, 31.62)
        
        p2 = ROOT.TLorentzVector()
        p2.SetPxPyPzE(-10, 0, -30, 31.62)
        
        # Combine them
        combined = p1 + p2
        
        # Check invariant mass
        assert combined.M() > 0
    except ImportError:
        pytest.skip("ROOT not available")


class TestParticlePhysics:
    """Tests for particle physics calculations"""
    
    def test_pt_calculation(self):
        """Test transverse momentum calculation"""
        px, py = 3.0, 4.0
        pt = math.sqrt(px**2 + py**2)
        assert pt == pytest.approx(5.0)
    
    def test_eta_calculation(self):
        """Test pseudorapidity calculation"""
        pz = 10.0
        pt = 5.0
        p = math.sqrt(pt**2 + pz**2)
        eta = 0.5 * math.log((p + pz) / (p - pz))
        assert eta > 0  # Forward direction
    
    def test_invariant_mass(self):
        """Test invariant mass of two-body system"""
        # Two photons going in opposite directions
        e1, px1 = 1.0, 1.0
        e2, px2 = 1.0, -1.0
        
        e_total = e1 + e2
        px_total = px1 + px2
        
        m_inv = math.sqrt(e_total**2 - px_total**2)
        assert m_inv == pytest.approx(2.0)


class TestDataStructures:
    """Tests for data handling"""
    
    def test_event_dict(self):
        """Test event as dictionary"""
        event = {
            "event_number": 42,
            "particles": [
                {"pt": 25.0, "eta": 1.2, "phi": 0.5},
                {"pt": 30.0, "eta": -0.8, "phi": 2.1},
            ]
        }
        assert len(event["particles"]) == 2
    
    def test_pt_cut(self):
        """Test pT selection"""
        particles = [
            {"pt": 15.0},
            {"pt": 25.0},
            {"pt": 35.0},
            {"pt": 10.0},
        ]
        
        selected = [p for p in particles if p["pt"] > 20.0]
        assert len(selected) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
