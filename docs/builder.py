import os, subprocess
from uuid import uuid4

def build_and_serve():
    project_dir = 'user_project'
    build_id = uuid4().hex
    archive = f'build_{build_id}.xcarchive'
    ipa_name = f'PyProgramz_{build_id}.ipa'
    ipa_path = os.path.join('docs', ipa_name)

    subprocess.check_call([
        'xcodebuild', '-project', f'{project_dir}/MyApp.xcodeproj',
        '-scheme', 'MyApp', 'archive', '-archivePath', archive,
        'CODE_SIGN_IDENTITY=' + os.getenv('CERT_NAME'),
        'PROVISIONING_PROFILE=' + os.getenv('PROVISIONING_PROFILE')
    ])
    export_dir = f'export_{build_id}'
    subprocess.check_call([
        'xcodebuild', '-exportArchive', '-archivePath', archive,
        '-exportOptionsPlist', 'docs/ExportOptions.plist', '-exportPath', export_dir
    ])
    os.makedirs('docs', exist_ok=True)
    exported = next(f for f in os.listdir(export_dir) if f.endswith('.ipa'))
    os.rename(os.path.join(export_dir, exported), ipa_path)

    ipa_url = f"https://purpleparrotpartpradime.github.io/The-PyProgramz/docs/" + ipa_name
    manifest_tpl = open('docs/manifest.plist').read()
    manifest = manifest_tpl.replace('{IPA_URL}', ipa_url)                           .replace('{BUNDLE_ID}', os.getenv('APP_BUNDLE_ID'))                           .replace('{VERSION}', os.getenv('APP_VERSION', '1.0'))
    with open('docs/manifest.plist', 'w') as m:
        m.write(manifest)
    return ipa_url
