# Appends a path to import python scripts that are in other directories.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/'))

import argparse
import sentencepiece as spm
from distutils.util import strtobool
from special_token_list import BOS_TOKEN, EOS_TOKEN, PAD_TOKEN, CLS_TOKEN, SEP_TOKEN, EOD_TOKEN, MASK_TOKEN, NEWLINE_TOKEN


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--model_prefix", type=str, required=True)
    parser.add_argument("--vocab_size", type=int, required=True)
    parser.add_argument("--input_sentence_size", type=int, required=True)
    parser.add_argument("--shuffle_input_sentence", type=lambda x: bool(strtobool(x)), required=True)
    parser.add_argument("--num_threads", type=int, required=True)
    parser.add_argument("--character_coverage", type=float, default=0.9995)
    parser.add_argument("--model_type", type=str, default="unigram", choices=["unigram", "bpe", "word", "char"])
    parser.add_argument("--train_extremely_large_corpus", type=lambda x: bool(strtobool(x)), default=True)
    args = parser.parse_args()
    print(f"{args = }")
    return args


def main():
    args = parse_arguments()

    # Trains a SentencePiece tokenizer. After training, *.model and *.vocab will be saved in the current directory.
    # https://github.com/llm-jp/llm-jp-tokenizer/blob/49f555459832cb8ed7eef132fd34e6eaa83bd077/scripts/createModel.py
    # https://github.com/llm-jp/llm-jp-tokenizer/blob/49f555459832cb8ed7eef132fd34e6eaa83bd077/scripts/howToCreateModel_ver2.md
    # https://drive.google.com/file/d/1Nj4P5NDMvYEy8juQwe6uSqgfYsCYa_E_/edit
    spm.SentencePieceTrainer.train(
        input=args.input,
        model_prefix=args.model_prefix,
        vocab_size=args.vocab_size,
        input_sentence_size=args.input_sentence_size,
        shuffle_input_sentence=args.shuffle_input_sentence,
        num_threads=args.num_threads,
        character_coverage=args.character_coverage,
        model_type=args.model_type,
        train_extremely_large_corpus=args.train_extremely_large_corpus,
        user_defined_symbols=[
            BOS_TOKEN,
            EOS_TOKEN,
            PAD_TOKEN,
            CLS_TOKEN,
            SEP_TOKEN,
            EOD_TOKEN,
            MASK_TOKEN,
            NEWLINE_TOKEN,
        ],  # Note: `NEWLINE_TOKEN` is needed in `user_defined_symbols`.
        byte_fallback=True,
        split_digits=True,
        allow_whitespace_only_pieces=True,
        remove_extra_whitespaces=False,
    )


if __name__ == "__main__":
    main()
