#!/bin/bash
# zpoolcli.sh — PAT-first where supported; JWT where required; SSH for ZFS.
# Clean command structure:
#   - claim <code>                 (JWT access)
#   - billing balance|ledger|start (JWT access; /dodo/start kept server-side)
#   - job, pat, sshkey, zpool      (JWTPAT or JWT as appropriate)
#   - zfs                          (SSH)

set -eo pipefail

# -----------------------------
# Config & defaults
# -----------------------------
DOTFILE="${HOME}/.config/zpools.io/zpoolrc"
API_DOMAIN="${API_DOMAIN:-}"
SSH_HOST="${SSH_HOST:-}"
SSH_PRIVKEY_FILE="${SSH_PRIVKEY_FILE:-}"
ZPOOLUSER="${ZPOOLUSER:-}"
ZPOOLPAT="${ZPOOLPAT:-}"   # optional; may come from env or rcfile
MAX_AGE_SECONDS="${MAX_AGE_SECONDS:-3600}"

# CLI overrides (non-empty only if provided)
CLI_USERNAME=""
CLI_PASSWORD=""

emit_json() {
  if command -v jq >/dev/null 2>&1; then
    if [[ -t 1 ]]; then
      jq -CrS . <<<"$1" || echo "$1"
    else
      jq -cS . <<<"$1" || echo "$1"
    fi
  else
    echo "$1"
  fi
}

die() {
  echo "Error: $*" >&2
  exit 1
}

note() {
  echo "$*" >&2
}

is_tty() {
  [[ -t 0 ]]
}

# -----------------------------
# Early option parsing (flags only)
# -----------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --rcfile)
      [[ -n "${2:-}" ]] || die "--rcfile requires a file path"
      [[ -f "$2" ]] || die "rcfile '$2' does not exist"
      DOTFILE="$2"
      shift 2
      ;;
    --username)
      [[ -n "${2:-}" ]] || die "--username requires a value"
      CLI_USERNAME="$2"
      shift 2
      ;;
    --password)
      [[ -n "${2:-}" ]] || die "--password requires a value"
      CLI_PASSWORD="$2"
      shift 2
      ;;
    --help|-h)
      # Defer to usage() so it can show rcfile-provided domains if set
      break
      ;;
    *)
      break
      ;;
  esac
done

# -----------------------------
# Load rcfile (no passwords)
# -----------------------------
if [[ -f "$DOTFILE" ]]; then
  eval "$(
    (
      # shellcheck source=/dev/null
      source "$DOTFILE"
      for var in API_DOMAIN BZFS_BIN LOCAL_POOL REMOTE_POOL SSH_HOST SSH_PRIVKEY_FILE ZPOOLUSER ZPOOLPAT; do
        val="${!var:-}"
        if [[ -n "$val" ]]; then
          printf 'if [[ -z "${%s:-}" ]]; then export %s=%q; fi\n' "$var" "$var" "$val"
        fi
      done
    )
  )"
fi

# -----------------------------
# Usage
# -----------------------------
usage() {
  echo
  echo "API: ${API_DOMAIN:-https://api.dev.zpools.io}    SSH: ${SSH_HOST:-ssh.dev.zpools.io}"
  echo
  echo "Commands (left column shows auth type; PAT-capable lines include required PAT scope):"
  echo
  echo "  === Identity & Codes ==="
  echo "  [JWT]     $0 claim <code>"
  echo
  echo "  === Billing ==="
  echo "  [JWT]     $0 billing balance"
  echo "  [JWT]     $0 billing ledger [since YYYY-MM-DD] [until YYYY-MM-DD] [limit (default 500)]"
  echo "  [JWT]     $0 billing start <amount_dollars>"
  echo
  echo "  === Personal Access Tokens ==="
  echo "  [JWTPAT]  $0 pat list                                  (scope: pat)"
  echo "  [JWT]     $0 pat create <label> [<soft-expiry YYYY-MM-DD>] [<tenant_id>] [scope1] [scope2] ..."
  echo "  [JWT]     $0 pat revoke <key_id>"
  echo
  echo "  === SSH Keys ==="
  echo "  [JWTPAT]  $0 sshkey list                               (scope: sshkey)"
  echo "  [JWT]     $0 sshkey add <public_key>"
  echo "  [JWT]     $0 sshkey delete <pubkey_id>"
  echo
  echo "  === Jobs ==="
  echo "  [JWTPAT]  $0 job list                                  (scope: job)"
  echo "  [JWTPAT]  $0 job show <job_id>                         (scope: job)"
  echo "  [JWTPAT]  $0 job history <job_id>                      (scope: job)"
  echo
  echo "  === Zpools ==="
  echo "  [JWTPAT]  $0 zpool list                                (scope: zpool)"
  echo "  [JWT]     $0 zpool create <new_size_in_gib> <volume_type>"
  echo "  [JWT]     $0 zpool delete <zpool_id>"
  echo "  [JWTPAT]  $0 zpool scrub <zpool_id>                    (scope: zpool)"
  echo "  [JWTPAT]  $0 zpool modify <zpool_id> <volume_type>     (scope: zpool)"
  echo "            (volume_type: gp3|sc1)"
  echo
  echo "  === Misc ==="
  echo "  [JWTPAT]  $0 hello                                     (scope: none)"
  echo
  echo "  === ZFS over SSH ==="
  echo "  [SSH]     $0 zfs list <dataset> [flags...]"
  echo "  [SSH]     $0 zfs destroy <dataset> [flags...]"
  echo "  [SSH]     $0 zfs snapshot <dataset@snapshot>"
  echo "  [SSH]     $0 zfs recv [flags...] <zpool/dataset>        (stdin: zfs send ...)"
  echo "  [SSH]     $0 zfs ssh [remote command...]"
  echo "  [SSH]     $0 zfs bzfs    (requires BZFS_BIN, LOCAL_POOL, REMOTE_POOL)"
  echo
  echo "Options:"
  echo "  --rcfile <path>       Load config variables from an alternate rcfile (default: ${DOTFILE})"
  echo "  --username <value>    Username for JWT auth when needed (overrides \$ZPOOLUSER just for this run)"
  echo "  --password <value>    Password for JWT auth when needed (non-interactive/CI)"
  echo
  echo "Notes:"
  echo "  • ZPOOLPAT is used automatically for PAT-capable endpoints ([JWTPAT]). If a PAT is rejected (401/403), the command fails and does not fall back to JWT."
  echo "  • No password is ever read from the rcfile. Username *may* be read (ZPOOLUSER)."
  echo "  • For endpoints requiring JWT, if creds are missing and stdin is not a TTY, the command errors out."
  echo "  • Required config if missing: set in ${DOTFILE} or export the env var:"
  echo "      API_DOMAIN         (e.g., https://api.dev.zpools.io)"
  echo "      SSH_HOST           (e.g., ssh.dev.zpools.io)"
  echo "      SSH_PRIVKEY_FILE   (path to your private key)"
  echo "      ZPOOLUSER          (username; can also pass via --username)"
  echo
  exit 1
}

# -----------------------------
# HTTP helpers
# -----------------------------
HTTP_STATUS=""
RESPONSE=""

do_http() {
  # do_http METHOD PATH AUTH_HEADER [JSON_BODY]
  local method="$1"
  local path="$2"
  local auth_header="$3"
  local data="${4:-}"
  local url="${API_DOMAIN}${path}"

  [[ -n "$API_DOMAIN" ]] || die "API_DOMAIN is required. Set it in ${DOTFILE} or export API_DOMAIN"

  local tmp
  tmp="$(mktemp)"
  if [[ -n "$data" ]]; then
    HTTP_STATUS="$(
      curl -s -o "$tmp" -w '%{http_code}' -X "$method" "$url" \
        -H "$auth_header" -H "Content-Type: application/json" \
        -d "$data"
    )"
  else
    HTTP_STATUS="$(
      curl -s -o "$tmp" -w '%{http_code}' -X "$method" "$url" \
        -H "$auth_header"
    )"
  fi
  RESPONSE="$(cat "$tmp")"
  rm -f "$tmp"
}

# -----------------------------
# Auth helpers (JWT only when needed)
# -----------------------------
token_file_for_user() {
  local user="$1"
  local domain
  domain=$(echo "$2" | sed -E 's#^https?://##; s#/.*##')
  echo "/dev/shm/zpool_token_${domain}_${user}"
}

prompt_username_if_needed() {
  if [[ -n "$CLI_USERNAME" ]]; then
    ZPOOLUSER="$CLI_USERNAME"
  fi
  if [[ -z "$ZPOOLUSER" ]]; then
    if is_tty; then
      read -r -p "Username: " ZPOOLUSER
    else
      die "Username required but not provided. Use --username or set ZPOOLUSER in ${DOTFILE}"
    fi
  fi
}

prompt_password_if_needed() {
  if [[ -n "$CLI_PASSWORD" ]]; then
    PASSWORD="$CLI_PASSWORD"
  else
    if is_tty; then
      read -r -s -p "zpools.io Password: " PASSWORD
      echo >&2
    else
      die "Password required but not provided. Use --password or run interactively"
    fi
  fi
}

login_and_cache_tokens() {
  local user="$1"
  local token_file; token_file="$(token_file_for_user "$user" "${API_DOMAIN}")"

  prompt_password_if_needed

  note "Authenticating to refresh token..."
  local auth_body
  auth_body=$(jq -n --arg u "$user" --arg p "$PASSWORD" '{username: $u, password: $p}')
  local tmp; tmp="$(mktemp)"
  local code
  code="$(
    curl -s -o "$tmp" -w '%{http_code}' -X POST "${API_DOMAIN}/login" \
      -H "Content-Type: application/json" \
      -d "$auth_body"
  )"
  local body; body="$(cat "$tmp")"; rm -f "$tmp"

  if [[ "$code" != "200" && "$code" != "201" ]]; then
    emit_json "$body"
    die "Authentication failed with HTTP $code"
  fi

  local access id expires
  access="$(jq -r '.detail.access_token // empty' <<<"$body")"
  id="$(jq -r '.detail.id_token // empty' <<<"$body")"
  expires="$(jq -r '.detail.expires_in // empty' <<<"$body")"

  [[ -n "$access" && -n "$id" && -n "$expires" ]] || {
    emit_json "$body"
    die "Login response missing required fields"
  }

  local expires_at
  expires_at=$(( $(date +%s) + expires ))

  umask 0177
  printf '{"access_token":"%s","id_token":"%s","expires_at":%s}\n' "$access" "$id" "$expires_at" >"$token_file"
  chmod 0600 "$token_file" || true
  note "Tokens refreshed."
}

ensure_jwt_fresh() {
  prompt_username_if_needed
  local token_file; token_file="$(token_file_for_user "$ZPOOLUSER" "${API_DOMAIN}")"

  if [[ -f "$token_file" ]]; then
    local file_json expires_at
    file_json="$(cat "$token_file")"
    expires_at="$(jq -r '.expires_at // 0' <<<"$file_json")"
    if (( $(date +%s) >= expires_at )); then
      login_and_cache_tokens "$ZPOOLUSER"
    fi
  else
    login_and_cache_tokens "$ZPOOLUSER"
  fi
}

bearer() {
  local kind="$1" # "access" or "id"
  local token_file; token_file="$(token_file_for_user "$ZPOOLUSER" "${API_DOMAIN}")"
  jq -r --arg k "${kind}_token" '.[$k]' "$token_file"
}

# -----------------------------
# API wrappers
# -----------------------------
api_pat_or_jwt_access() {
  # api_pat_or_jwt_access METHOD PATH [JSON_BODY]
  local method="$1"
  local path="$2"
  local data="${3:-}"

  if [[ -n "$ZPOOLPAT" ]]; then
    do_http "$method" "$path" "Authorization: Bearer ${ZPOOLPAT}" "$data"
    if [[ "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]]; then
      emit_json "$RESPONSE"
      return 0
    elif [[ "$HTTP_STATUS" == "401" || "$HTTP_STATUS" == "403" ]]; then
      emit_json "$RESPONSE"
      die "PAT was rejected with HTTP ${HTTP_STATUS}. Fix ZPOOLPAT or remove it to use JWT."
    else
      emit_json "$RESPONSE"
      die "Request failed with HTTP ${HTTP_STATUS}"
    fi
  fi

  ensure_jwt_fresh
  do_http "$method" "$path" "Authorization: Bearer $(bearer access)" "$data"
  emit_json "$RESPONSE"
}

api_jwt_access() {
  # api_jwt_access METHOD PATH [JSON_BODY]
  local method="$1"
  local path="$2"
  local data="${3:-}"
  ensure_jwt_fresh
  do_http "$method" "$path" "Authorization: Bearer $(bearer access)" "$data"
  emit_json "$RESPONSE"
}

# -----------------------------
# Command groups
# -----------------------------
billing_operations() {
  case "$1" in
    balance)
      api_jwt_access GET "/billing/balance"
      ;;
    ledger)
      # billing ledger [since] [until] [limit]
      local since="${2:-}"
      local until="${3:-}"
      local limit="${4:-}"
      local qs=()
      [[ -n "$since" ]] && qs+=("since=${since}")
      [[ -n "$until" ]] && qs+=("until=${until}")
      [[ -n "$limit" ]] && qs+=("limit=${limit}")
      local query=""
      if (( ${#qs[@]} )); then
        query="?$(IFS='&'; echo "${qs[*]}")"
      fi
      api_jwt_access GET "/billing/ledger${query}"
      ;;
    start)
      # billing start <amount_dollars>
      [[ -n "${2:-}" ]] || die "Missing amount for billing start. Usage: $0 billing start <amount_dollars>"
      local amount_dollars="$2"
      # REST API unchanged: still POST /dodo/start with 'quantity'
      local payload
      payload="$(jq -n --argjson q "$amount_dollars" '{quantity:$q}')"
      api_jwt_access POST "/dodo/start" "$payload"
      ;;
    usage|help|--help|-h|*)
      echo
      echo "Billing commands:"
      echo "  $0 billing balance"
      echo "  $0 billing ledger [since YYYY-MM-DD] [until YYYY-MM-DD] [limit]"
      echo "  $0 billing start <amount_dollars>"
      echo
      exit 1
      ;;
  esac
}

claim_operation() {
  # claim <code>
  [[ -n "${1:-}" ]] || die "Missing code for claim."
  local claim_code="$1"

  _open_url() {
    local url="$1"
    if command -v xdg-open >/dev/null 2>&1; then xdg-open "$url" >/dev/null 2>&1 || true
    elif command -v open >/dev/null 2>&1; then open "$url" >/dev/null 2>&1 || true
    elif command -v start >/dev/null 2>&1; then start "$url" >/dev/null 2>&1 || true
    else
      note "No system opener found (xdg-open/open/start)."
      return 1
    fi
  }

  _copy_url() {
    local url="$1"
    if command -v pbcopy >/dev/null 2>&1; then printf %s "$url" | pbcopy && note "URL copied to clipboard (pbcopy)." && return 0; fi
    if command -v xclip  >/dev/null 2>&1; then printf %s "$url" | xclip -selection clipboard && note "URL copied to clipboard (xclip)." && return 0; fi
    if command -v xsel   >/dev/null 2>&1; then printf %s "$url" | xsel --clipboard --input && note "URL copied to clipboard (xsel)." && return 0; fi
    if command -v clip.exe >/dev/null 2>&1; then printf %s "$url" | clip.exe && note "URL copied to clipboard (clip.exe)." && return 0; fi
    note "No clipboard tool found (pbcopy/xclip/xsel/clip.exe)."
    return 1
  }

  _view_in_pager() {
    local url="$1"
    local pager="${PAGER:-}"
    if [[ -z "$pager" ]]; then
      if command -v less >/dev/null 2>&1; then pager="less -R"
      elif command -v more >/dev/null 2>&1; then pager="more"
      else pager="cat"
      fi
    fi
    curl -fsSL "$url" | eval "$pager"
  }

  ensure_jwt_fresh
  local payload; payload="$(jq -n --arg c "$claim_code" '{code:$c}')"
  do_http POST "/codes/claim" "Authorization: Bearer $(bearer access)" "$payload"

  if [[ "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]]; then
    emit_json "$RESPONSE"
    return 0
  fi

  if [[ "$HTTP_STATUS" == "428" ]]; then
    is_tty || die "Interactive TTY required to accept Terms. Re-run in a terminal."
    local tos_url
    tos_url="$(jq -r '.detail.tos_url // empty' <<<"$RESPONSE")"
    [[ -n "$tos_url" ]] || { emit_json "$RESPONSE"; die "Server did not provide tos_url."; }

    echo
    echo "This code requires accepting Terms of Service."
    echo "URL: $tos_url"
    echo
    echo "Choose an action:"
    echo "  [O] Open in your default browser"
    echo "  [V] View in this terminal (pager)"
    echo "  [C] Copy URL to clipboard"
    echo "  [P] Print URL again"
    echo

    while true; do
      read -r -p "Select action (O/V/C/P), or press Enter to continue to acceptance prompt: " act
      case "$(tr '[:lower:]' '[:upper:]' <<<"${act}")" in
        O) _open_url "$tos_url" || true ;;
        V) _view_in_pager "$tos_url" ;;
        C) _copy_url "$tos_url" || true ;;
        P) echo "URL: $tos_url" ;;
        "") break ;;
        *) echo "Unknown choice. Use O/V/C/P or Enter." ;;
      esac
    done

    echo
    read -r -p "Type YES to accept the Terms exactly as published at the URL above: " ack
    if [[ "$ack" != "YES" ]]; then
      die "Terms not accepted."
    fi

    local accepted_at
    accepted_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    local commit_payload
    commit_payload="$(
      jq -n \
        --arg c "$claim_code" \
        --arg u "$tos_url" \
        --arg t "$accepted_at" \
        '{code:$c, tos:{url:$u, accepted_at:$t}}'
    )"

    do_http POST "/codes/claim" "Authorization: Bearer $(bearer access)" "$commit_payload"
    emit_json "$RESPONSE"
    [[ "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]] || exit 1
    return 0
  fi

  emit_json "$RESPONSE"
  exit 1
}

job_operations() {
  case "$1" in
    list)    api_pat_or_jwt_access GET "/jobs" ;;
    show)    [[ -n "${2:-}" ]] || die "Missing job_id for job show."; api_pat_or_jwt_access GET "/job/$2" ;;
    history) [[ -n "${2:-}" ]] || die "Missing job_id for job history."; api_pat_or_jwt_access GET "/job/$2/history" ;;
    usage|help|--help|-h|*)
      echo
      echo "Jobs:"
      echo "  $0 job list"
      echo "  $0 job show <job_id>"
      echo "  $0 job history <job_id>"
      echo
      echo "Example of some useful commands:"
      echo
      echo "  List all recent jobs, their type, and parameters"
      echo "    ./zpoolcli.sh job list | jq '.detail.jobs' | mlr --ijson --opprint put '\$last_ts = \$current_status.timestamp' \\"
      echo "      then cut -o -f created_at,last_ts,job_id,job_type,parameters | sort -n"
      echo
      echo "  Showing all the events from a job in tabular form (requires 'mlr'):"
      echo "    ./zpoolcli.sh job history <job_id> | jq '.detail.history' | mlr --ijson --opprint cut -o -f timestamp,event_type,message"
      exit 1
      ;;
  esac
}

pat_operations() {
  case "$1" in
    list)
      api_pat_or_jwt_access GET "/pat"
      ;;
    create)
      [[ -n "${2:-}" ]] || die "Missing <label> for pat create."
      local label="$2"
      local expiry="${3:-}"
      local tenant_id="${4:-}"
      local scopes_json=""
      if [[ $# -ge 5 ]]; then
        scopes_json="$(printf '%s\n' "${@:5}" | jq -R . | jq -s .)"
      fi
      local payload
      if [[ -n "$scopes_json" ]]; then
        payload="$(
          jq -n --arg lbl "$label" --arg expiry "$expiry" --arg tenant "$tenant_id" --argjson scopes "$scopes_json" '
            {"label": $lbl}
            + (if ($expiry|length)>0 then {"expiry": $expiry} else {} end)
            + (if ($tenant|length)>0 then {"tenant_id": $tenant} else {} end)
            + (if ($scopes|length)>0 then {"scopes": $scopes} else {} end)
          '
        )"
      else
        payload="$(
          jq -n --arg lbl "$label" --arg expiry "$expiry" --arg tenant "$tenant_id" '
            {"label": $lbl}
            + (if ($expiry|length)>0 then {"expiry": $expiry} else {} end)
            + (if ($tenant|length)>0 then {"tenant_id": $tenant} else {} end)
          '
        )"
      fi
      api_jwt_access POST "/pat" "$payload"
      ;;
    revoke)
      [[ -n "${2:-}" ]] || die "Missing <key_id> for pat revoke."
      api_jwt_access DELETE "/pat/$2"
      ;;
    usage|help|--help|-h|*)
      echo
      echo "PAT:"
      echo "  $0 pat list"
      echo "  $0 pat create <label> [<soft-expiry YYYY-MM-DD>] [<tenant_id>] [scope1] [scope2] ..."
      echo "  $0 pat revoke <key_id>"
      echo
      exit 1
      ;;
  esac
}

sshkey_operations() {
  case "$1" in
    list)   api_pat_or_jwt_access GET "/sshkey" ;;
    add)    [[ -n "${2:-}" ]] || die "Missing public_key for sshkey add."; api_jwt_access POST "/sshkey" "$(jq -n --arg k "$2" '{pubkey:$k}')" ;;
    delete) [[ -n "${2:-}" ]] || die "Missing pubkey_id for sshkey delete."; api_jwt_access DELETE "/sshkey/$2" ;;
    usage|help|--help|-h|*)
      echo
      echo "SSH Keys:"
      echo "  $0 sshkey list"
      echo "  $0 sshkey add '<public_key>'"
      echo "  $0 sshkey delete <pubkey_id>"
      echo
      exit 1
      ;;
  esac
}

zpool_operations() {
  case "$1" in
    list)    api_pat_or_jwt_access GET "/zpools" ;;
    create)  [[ -n "${2:-}" && -n "${3:-}" ]] || die "Missing args for zpool create."
             api_jwt_access POST "/zpool" "$(jq -n --argjson s "$2" --arg v "$3" '{new_size_in_gib:$s, volume_type:$v}')" ;;
    delete)  [[ -n "${2:-}" ]] || die "Missing zpool_id for delete."
             api_jwt_access DELETE "/zpool/$2" ;;
    scrub)   [[ -n "${2:-}" ]] || die "Missing zpool_id for scrub."
             api_pat_or_jwt_access POST "/zpool/$2/scrub" ;;
    modify)  [[ -n "${2:-}" && -n "${3:-}" ]] || die "Usage: $0 zpool modify <zpool_id> <volume_type: gp3|sc1>"
             local zpid="$2"
             local vt; vt="$(tr '[:upper:]' '[:lower:]' <<<"$3")"
             case "$vt" in gp3|sc1) ;; *) die "Invalid volume_type '$3'. Allowed: gp3, sc1" ;; esac
             local payload; payload="$(jq -n --arg vt "$vt" '{target_volume_type:$vt, volume_type:$vt}')"
             api_pat_or_jwt_access POST "/zpool/${zpid}/modify" "$payload" ;;
    usage|help|--help|-h|*)
      echo
      echo "Zpools:"
      echo "  $0 zpool list"
      echo "  $0 zpool create <new_size_in_gib> <volume_type>"
      echo "  $0 zpool delete <zpool_id>"
      echo "  $0 zpool scrub <zpool_id>"
      echo "  $0 zpool modify <zpool_id> <gp3|sc1>"
      echo
      exit 1
      ;;
  esac
}

function sync_bzfs() {
    _LOCAL_POOL="${1}"
    _REMOTE_POOL="${2}"
    "${BZFS_BIN}" "${_LOCAL_POOL}" "${_REMOTE_POOL}" \
      --recursive \
      --include-snapshot-regex 'autosnap_.*_(daily|monthly)$' \
      --delete-dst-snapshots=snapshots \
      --delete-dst-snapshots-no-crosscheck \
      --no-privilege-elevation
}

zfs_operations() {
  local zfs_cmd="$1"; shift || true

  [[ -n "$SSH_HOST" ]] || die "SSH_HOST is required for zfs ops. Set it in ${DOTFILE} or export SSH_HOST."
  [[ -n "$SSH_PRIVKEY_FILE" ]] || die "SSH_PRIVKEY_FILE is required for zfs ops. Set it in ${DOTFILE} or export SSH_PRIVKEY_FILE."
  [[ -f "$SSH_PRIVKEY_FILE" ]] || die "SSH_PRIVKEY_FILE '$SSH_PRIVKEY_FILE' not found."
  if [[ -z "$ZPOOLUSER" ]]; then
    if is_tty; then
      read -r -p "ZFS SSH username (ZPOOLUSER): " ZPOOLUSER
    else
      die "ZPOOLUSER required for zfs ops. Set it in ${DOTFILE} or export ZPOOLUSER."
    fi
  fi

  case "$zfs_cmd" in
    bzfs)
      [[ -n "$BZFS_BIN" ]] || die "BZFS_BIN is required for bzfs sync. Set it in ${DOTFILE} or export BZFS_BIN."
      [[ -n "$LOCAL_POOL" ]] || die "LOCAL_POOL is required for bzfs sync. Set it in ${DOTFILE} or export LOCAL_POOL."
      [[ -n "$REMOTE_POOL" ]] || die "REMOTE_POOL is required for bzfs sync. Set it in ${DOTFILE} or export REMOTE_POOL."
      sync_bzfs "${LOCAL_POOL}" "${REMOTE_POOL}"
      ;;
    list)
      [[ -n "${1:-}" ]] || die "Missing dataset for zfs list."
      local dataset="$1"; shift || true
      ssh -i "$SSH_PRIVKEY_FILE" "$ZPOOLUSER@$SSH_HOST" zfs list "$dataset" "$@"
      ;;
    destroy)
      [[ -n "${1:-}" ]] || die "Missing dataset for zfs destroy."
      local dataset="$1"; shift || true
      ssh -i "$SSH_PRIVKEY_FILE" "$ZPOOLUSER@$SSH_HOST" zfs destroy "$dataset" "$@"
      ;;
    snapshot)
      [[ -n "${1:-}" ]] || die "Missing dataset@snapshot for zfs snapshot."
      local snap="$1"
      ssh -i "$SSH_PRIVKEY_FILE" "$ZPOOLUSER@$SSH_HOST" zfs snapshot "$snap"
      ;;
    recv)
      (( $# >= 1 )) || { echo; echo "Usage: zfs send localpool/ds@snap | $0 zfs recv [flags...] <zpool/dataset>"; echo; exit 1; }
      local full_dataset="${@: -1}"
      local recv_flags=("${@:1:$#-1}")
      ssh -i "$SSH_PRIVKEY_FILE" "$ZPOOLUSER@$SSH_HOST" zfs recv "${recv_flags[@]}" "$full_dataset"
      ;;
    ssh)
      ssh -i "$SSH_PRIVKEY_FILE" "$ZPOOLUSER@$SSH_HOST" "$@"
      ;;
    usage|help|--help|-h|*)
      echo
      echo "ZFS over SSH:"
      echo "  $0 zfs list <dataset> [flags...]"
      echo "  $0 zfs destroy <dataset> [flags...]"
      echo "  $0 zfs snapshot <dataset@snapshot>"
      echo "  zfs send localpool/ds@snap | $0 zfs recv [flags...] <zpool/dataset>"
      echo "  $0 zfs ssh"
      echo "  $0 zfs bzfs"
      echo
      exit 1
      ;;
  esac
}

# -----------------------------
# Main
# -----------------------------
[[ -n "${1:-}" ]] || { echo "Error: No command provided." >&2; usage; }

case "$1" in
  billing)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for billing." >&2; billing_operations usage; }
    billing_operations "$@"
    ;;
  claim)
    shift
    claim_operation "$@"
    ;;
  hello)
    api_pat_or_jwt_access GET "/hello"
    ;;
  job)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for job." >&2; job_operations usage; }
    job_operations "$@"
    ;;
  pat)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for pat." >&2; pat_operations usage; }
    pat_operations "$@"
    ;;
  sshkey)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for sshkey." >&2; sshkey_operations usage; }
    sshkey_operations "$@"
    ;;
  zfs)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for zfs." >&2; zfs_operations usage; }
    zfs_operations "$@"
    ;;
  zpool)
    shift
    [[ -n "${1:-}" ]] || { echo "Error: Missing operation for zpool." >&2; zpool_operations usage; }
    zpool_operations "$@"
    ;;
  usage|help|--help|-h)
    usage
    ;;
  *)
    echo "Error: Unknown command '$1'." >&2
    usage
    ;;
esac
