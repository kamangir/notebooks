#! /usr/bin/env bash

function abcli_docker() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "@docker browse [~public]" \
            "browse docker-hub"

        abcli_show_usage "@docker build [dryrun,~push,run]" \
            "build abcli docker image."

        abcli_show_usage "@docker clear" \
            "clear docker."

        abcli_docker eval "$@"

        abcli_show_usage "@docker push" \
            "push abcli docker image."

        abcli_show_usage "@docker run [dryrun]" \
            "run abcli docker image."

        abcli_show_usage "@docker seed" \
            "seed docker 🌱."

        abcli_docker source "$@"
        return
    fi

    local options=$2
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local filename="Dockerfile"

    if [ "$task" == "browse" ]; then
        local show_public=$(abcli_option_int "$options" public 1)

        local url=https://hub.docker.com/repository/docker/kamangir/abcli/general
        [[ "$show_public" == 1 ]] &&
            local url=https://hub.docker.com/r/kamangir/abcli/tags

        abcli_browse_url $url
        return
    fi

    if [ "$task" == "build" ]; then
        abcli_log "docker: building $filename: $options"

        local do_push=$(abcli_option_int "$options" push $(abcli_not $do_dryrun))
        local do_run=$(abcli_option_int "$options" run 0)

        pushd $abcli_path_git >/dev/null

        mkdir -p temp
        cp -v ~/.kaggle/kaggle.json temp/

        abcli_eval ,$options \
            docker build \
            --build-arg HOME=$HOME \
            -t kamangir/abcli \
            -f notebooks-and-scripts/$filename \
            .

        rm -rfv temp

        [[ "$do_push" == "1" ]] &&
            abcli_docker push $options

        [[ "$do_run" == "1" ]] &&
            abcli_docker run $options

        popd >/dev/null

        return
    fi

    if [ "$task" == "clear" ]; then
        abcli_eval ,$options \
            "docker image prune"
        abcli_eval ,$options \
            "docker system prune"
        return
    fi

    if [ "$task" == "push" ]; then
        abcli_eval ,$options \
            docker push \
            kamangir/abcli:latest
        return
    fi

    if [ "$task" == "run" ]; then
        abcli_log "docker: running $filename: $options"

        abcli_eval dryrun=$do_dryrun,path=$abcli_path_nbs \
            docker-compose run abcli bash \
            --init-file /root/git/awesome-bash-cli/bash/abcli.sh

        return
    fi

    if [ "$task" == "seed" ]; then
        abcli_seed docker "${@:2}"
        return
    fi

    [[ "$task" == evaluate ]] && task=eval
    if [[ "|eval|source|" == *"|$task|"* ]]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            [[ "$task" == "eval" ]] &&
                abcli_show_usage "@docker eval $EOP[$abcli_scripts_options]$EOPE$ABCUL<command-line>" \
                    "run <command-line> through the abcli docker image."

            [[ "$task" == "source" ]] &&
                abcli_show_usage "@docker source $EOP[$abcli_scripts_options]$EOPE$ABCUL<script-name> [<args>]" \
                    "source <script-name> <args> through the abcli docker image."

            return
        fi

        local command_line
        [[ "$task" == "eval" ]] &&
            command_line="source \
            /root/git/awesome-bash-cli/bash/abcli.sh install,mono \
            abcli_eval $options \
            ${@:3}"
        [[ "$task" == "source" ]] &&
            command_line="source \
            /root/git/awesome-bash-cli/bash/abcli.sh install,mono \
            abcli_scripts source $options \
            ${@:3}"

        abcli_eval dryrun=$do_dryrun,path=$abcli_path_nbs \
            docker-compose run abcli \
            bash -c \"$command_line\"

        return
    fi

    abcli_log_error "-abcli: docker: $task: command not found."
    return 1
}
