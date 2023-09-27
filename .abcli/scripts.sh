#! /usr/bin/env bash

function scripts() {
    abcli_scripts "$@"
}

function abcli_scripts() {
    local task=$(abcli_unpack_keyword $1 code)

    if [ "$task" == "help" ]; then
        abcli_log "📜 $(python3 -m notebooks_and_scripts version --show_description 1)\n"

        abcli_show_usage "abcli scripts list" \
            "list scripts."

        abcli_show_usage "abcli scripts source$ABCUL[<script-name>]$ABCUL<args>" \
            "source <script-name>.sh"
        return
    fi

    local function_name=abcli_scripts_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name ${@:2}
    fi

    if [[ ",ls,list," == *",$task,"* ]]; then
        local path=$abcli_path_git/notebooks-and-scripts/scripts

        local filename=$2
        [[ ! -z "$filename" ]] &&
            local path=$path/$filename

        if [[ -f "$path" ]]; then
            abcli_log_file $path
        else
            abcli_log "🔗 $path"
            ls -1 $path \
                "${@:3}"
        fi

        return
    fi

    if [ "$task" == "source" ]; then
        local script_name=$(abcli_clarify_input $2 script)

        chmod +x $script_name.sh
        source $script_name.sh
        return
    fi

    abcli_log_error "-abcli: script: $task: command not found."
}
