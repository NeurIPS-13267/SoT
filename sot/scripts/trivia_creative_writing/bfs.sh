python run.py \
    --task trivia_creative_writing \
    --task_start_index 0 \
    --task_end_index 10 \
    --method_generate writing \
    --method_evaluate writing \
    --method_select writing \
    --n_generate_sample 3 \
    --n_evaluate_sample 1 \
    --n_select_sample 1 \
    --prompt_sample cot \
    --temperature 0.1 \
    --backend gpt-3.5-turbo \
    ${@}

# 0.3 dollars per line ->  30 dollars for 100 lines
