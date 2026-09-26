from __future__ import annotations
import argparse, json
from pathlib import Path
from .config import DEFAULT_CONFIG, load_config
from .downloader import download
from .manifest import build_manifest, verify_manifest
from .normalization import normalize_dataset
from .profile import profile

ROOT = Path(__file__).resolve().parents[3]
def paths(dataset): return ROOT / "data/raw" / dataset, ROOT / "data/derived" / dataset, ROOT / "data/manifests" / f"{dataset}_manifest.json"
def main() -> None:
    parser = argparse.ArgumentParser(description="Acquire and normalize immutable FlyWire FAFB v783 artifacts.")
    parser.add_argument("command", choices=["validate-config", "acquire", "manifest", "verify", "normalize", "profile"])
    parser.add_argument("dataset", nargs="?", default="fafb_v783", choices=["fafb_v783"])
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(); config = load_config(args.config); raw, derived, manifest = paths(args.dataset)
    if args.command == "validate-config":
        required = {"dataset_id", "name", "version", "sex", "coverage", "source_id", "source_url", "license", "files"}
        if missing := required - config.keys(): raise SystemExit(f"invalid configuration, missing: {sorted(missing)}")
        print("configuration valid"); return
    if args.command == "acquire":
        for spec in config["files"]:
            if not spec.get("source_url"): raise SystemExit("FAFB v783 bulk exports require the documented official manual/API acquisition step; see docs/datasets/fafb_v783.md")
            download(spec["source_url"], raw / spec["filename"], spec.get("expected_sha256"))
        build_manifest(config, raw, manifest); print(manifest); return
    if args.command == "manifest":
        print(build_manifest(config, raw, manifest)); return
    if args.command == "verify":
        failures = verify_manifest(manifest)
        if failures: raise SystemExit("\n".join(failures))
        print("manifest verified"); return
    if args.command == "normalize":
        result = normalize_dataset(config, raw, derived); print(json.dumps(result, indent=2)); return
    print(json.dumps(profile(derived), indent=2, sort_keys=True))
if __name__ == "__main__": main()
