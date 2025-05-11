import os, subprocess, json

def build_and_serve():
    # Load config from docs/config.json
    with open('docs/config.json') as f:
        cfg = json.load(f)

    project_dir = 'user_project'
    build_id = __import__('uuid').uuid4().hex
    archive = f'build_{build_id}.xcarchive'
    ipa_name = f'PyProgramz_{build_id}.ipa'
    ipa_path = os.path.join('docs', ipa_name)

    subprocess.check_call([
        'xcodebuild', '-project', f'{project_dir}/MyApp.xcodeproj',
        '-scheme', 'MyApp', 'archive', '-archivePath', archive,
        'CODE_SIGN_IDENTITY=' + cfg['cert_name'],
        'PROVISIONING_PROFILE=' + cfg['provisioning_profile']
    ])
    export_dir = f'export_{build_id}'
    subprocess.check_call([
        'xcodebuild', '-exportArchive', '-archivePath', archive,
        '-exportOptionsPlist', 'docs/ExportOptions.plist', '-exportPath', export_dir
    ])
    os.makedirs('docs', exist_ok=True)
    exported = next(f for f in os.listdir(export_dir) if f.endswith('.ipa'))
    os.rename(os.path.join(export_dir, exported), ipa_path)

    ipa_url = f"https://{cfg['hostname']}/docs/" + ipa_name
    manifest_tpl = open('docs/manifest.plist').read()
    manifest = manifest_tpl.replace('{{IPA_URL}}', ipa_url)                           .replace('{{BUNDLE_ID}}', cfg['bundle_id'])                           .replace('{{VERSION}}', cfg.get('app_version', '1.0'))
    with open('docs/manifest.plist', 'w') as m:
        m.write(manifest)
    return ipa_url
