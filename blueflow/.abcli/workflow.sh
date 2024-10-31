#! /usr/bin/env bash

function notebooks_and_scripts_workflow() {
    local task=$(abcli_unpack_keyword $1)

    local function_name=notebooks_and_scripts_workflow_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "workflow: $task: command not found."
    return 1
}

abcli_source_caller_suffix_path /workflow
