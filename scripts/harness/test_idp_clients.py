"""The browser OIDC client lists every front origin exactly, and nothing wider (lab ADR-001, SEC-002)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("idp_clients", ROOT / "ops/stack/idp_clients.py")
idp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(idp)

PAGES = "https://supportops-console.pages.dev"
LOCAL = "http://localhost:48080"


class OriginParsing(unittest.TestCase):
    def test_single_origin_keeps_working(self):
        self.assertEqual(idp.parse_origins(LOCAL + "/"), [LOCAL])

    def test_several_origins_are_split_trimmed_and_deduplicated(self):
        self.assertEqual(idp.parse_origins(f" {PAGES} , {LOCAL},{PAGES}/ "), [PAGES, LOCAL])

    def test_unsafe_values_are_refused(self):
        for bad in ("*", "https://*.pages.dev", "https://a.example/app", "http://public.example", "ftp://a.example", "", " , "):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    idp.parse_origins(bad)


class ClientDocument(unittest.TestCase):
    def test_every_origin_gets_a_redirect_a_web_origin_and_a_logout_uri(self):
        doc = idp.client_document([PAGES, LOCAL])
        self.assertEqual(doc["redirectUris"], [PAGES + "/", LOCAL + "/"])
        self.assertEqual(doc["webOrigins"], [PAGES, LOCAL])
        self.assertEqual(doc["attributes"]["post.logout.redirect.uris"], f"{PAGES}/##{LOCAL}/")
        self.assertEqual(doc["rootUrl"], PAGES)

    def test_client_stays_public_pkce_without_direct_grants(self):
        doc = idp.client_document([PAGES])
        self.assertTrue(doc["publicClient"])
        self.assertFalse(doc["directAccessGrantsEnabled"])
        self.assertFalse(doc["implicitFlowEnabled"])
        self.assertEqual(doc["attributes"]["pkce.code.challenge.method"], "S256")

    def test_no_wildcard_ever_reaches_the_document(self):
        doc = idp.client_document([PAGES, LOCAL])
        self.assertNotIn("*", str(doc["redirectUris"]) + str(doc["webOrigins"]))


if __name__ == "__main__":
    unittest.main()
