#! /usr/bin/env bash

function cat_under_trees() {
    local options=$1

    local list_of_artists="Leonardo-da-Vinci,Vincent-van-Gogh,Michelangelo,Gustav-Klimt,Claude-Monet,Paul-Cézanne,Frida-Kahlo,Salvador-Dali,Jackson-Pollock,Johannes-Vermeer,Wassily-Kandinsky,Edvard-Munch,Paul-Gauguin,Pablo-Picasso,Rembrandt,Diego-Velázquez,Henri-Matisse,Andy-Warhol,Edgar-Degas,J.-M.-W.-Turner,Caravaggio"

    local sentence="a cat walking under apple trees"

    local script_name=$(basename "${BASH_SOURCE[0]}")
    local script_name=${script_name%.*}

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="$abcli_scripts_options,count=<-1>"
        abcli_show_usage "abcli scripts source $script_name$ABCUL[$options]$ABCUL[<object-name>]$ABCUL[\"$sentence\"]$ABCUL[$args]" \
            "paint a sentence by different artists."

        abcli_log_list "$list_of_artists" , "artists(s)"
        return
    fi

    local count=$(abcli_option "$options" count -1)
    [[ "$count" != -1 ]] &&
        local list_of_artists=$(abcli_list_size $list_of_artists $count)
    abcli_log_list "$list_of_artists" , "artists(s)"

    local sentence=${3:-$sentence}
    abcli_log "painting $sentence ..."

    local artist
    for artist in $(echo $list_of_artists | tr , " "); do

        local filename=$(python3 -c "print('$artist'.lower().replace(' ','-'))")

        blue_stability generate image \
            ~dryrun \
            $filename \
            - \
            "$sentence style by $(echo $artist | tr - " ")"
    done

    abcli_log "completed."
}

cat_under_trees "$@"
