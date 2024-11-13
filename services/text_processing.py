import jieba
from tqdm import tqdm
from models import Example, ExampleLink, Vocab, db
from services.dictionary_service import get_word_meaning, get_word_meaning as get_sentence_meaning
import re ,os
# os.system("python -m pip install PyMultiDictionary")
# from PyMultiDictionary import MultiDictionary

# dictionary = MultiDictionary()
# x=dictionary.translate("zh", "射程", to="vi")[-2][1]
# print('x=',x)
# def analyze_text(text, user):
#     cleaned_text = re.sub(r"[^A-Za-z\u4e00-\u9fff\s]", "", text)
#     words = jieba.cut(cleaned_text)
#     new_words = []

#     for word in words:
#         if not Vocab.query.filter_by(word=word, user_id=user.id).first():
#             pinyin_text, meaning = get_word_meaning(word)
#             if pinyin_text:
#                 new_word = Vocab(word=word, meaning=meaning,pinyin_text=pinyin_text, user_id=user.id)
#                 db.session.add(new_word)
#                 new_words.append({"word": word, "pinyin_text":pinyin_text, "meaning": meaning})


#     db.session.commit()
#     return new_words
# def analyze_text(text, user):
#     cleaned_text = re.sub(r"[^A-Za-z\u4e00-\u9fff\s]", "", text)
#     words = jieba.cut(cleaned_text)
#     new_words = []

#     # Tách đoạn văn thành các câu đơn
#     sentences = re.split(r"[。！？.!?；]", text)

#     for word in words:
#         vocab_entry = Vocab.query.filter_by(word=word, user_id=user.id).first()

#         if vocab_entry:
#             # Nếu từ đã tồn tại trong Vocab, thêm câu làm ví dụ nếu có chứa từ đó
#             for sentence in sentences:
#                 if word in sentence:
#                     sentence_pinyin, sentence_meaning = get_sentence_meaning( sentence, splitter=' ' )
#                     example = Example(
#                         vocab_id=vocab_entry.id,
#                         chinese_text=sentence,
#                         pinyin_text=sentence_pinyin,
#                         meaning=sentence_meaning,
#                     )
#                     db.session.add(example)

#         else:
#             # Nếu từ chưa tồn tại, thêm từ vào bảng Vocab và tìm câu đầu tiên làm ví dụ
#             pinyin_text, meaning = get_word_meaning(word)
#             if pinyin_text:
#                 new_vocab = Vocab(
#                     word=word, meaning=meaning, pinyin_text=pinyin_text, user_id=user.id
#                 )
#                 db.session.add(new_vocab)
#                 db.session.flush()  # Lấy id của từ mới thêm vào

#                 # Tìm câu đầu tiên chứa từ và thêm làm ví dụ
#                 for sentence in sentences:
#                     if word in sentence:
#                         sentence_pinyin, sentence_meaning = get_sentence_meaning( sentence, splitter=' ' )
#                         example = Example(
#                             vocab_id=new_vocab.id,
#                             chinese_text=sentence,
#                             pinyin_text=sentence_pinyin,
#                             meaning=sentence_meaning,
#                         )
#                         db.session.add(example)
#                         break  # Chỉ thêm một câu làm ví dụ đầu tiên cho từ mới

#                 new_words.append(
#                     {"word": word, "pinyin_text": pinyin_text, "meaning": meaning}
#                 )

#     db.session.commit()
#     return new_words


def analyze_text(text, user):
    cleaned_text = re.sub(r"[^A-Za-z\u4e00-\u9fff\s]", "", text)
    words = jieba.cut(cleaned_text)
    new_words = []

    sentences = re.split(r"[。！？.!?]", text)
    N=0
    for word in words:
        N+=1
    words = jieba.cut(cleaned_text)
    for _ in tqdm(range(N)):
        word = next(words)            
        vocab_entry = Vocab.query.filter_by(word=word, user_id=user.id).first()

        if not vocab_entry:
            # Từ mới, thêm vào bảng Vocab
            pinyin_text, meaning = get_word_meaning(word)
            if pinyin_text:
                vocab_entry = Vocab(
                    word=word, meaning=meaning, pinyin_text=pinyin_text, user_id=user.id
                )
                db.session.add(vocab_entry)
                db.session.flush()  # Lấy id của từ mới thêm vào
                new_words.append(
                    {"word": word, "pinyin_text": pinyin_text, "meaning": meaning}
                )

        # Thêm ví dụ cho từ
        for sentence in sentences:
            if word in sentence:
                # Kiểm tra câu đã tồn tại trong Example chưa
                existing_example = Example.query.filter_by(
                    chinese_text=sentence
                ).first()

                if not existing_example:
                    # Nếu câu chưa tồn tại, thêm mới
                    sentence_pinyin, sentence_meaning = get_sentence_meaning(sentence, splitter=' ')
                    example = Example(
                        chinese_text=sentence,
                        pinyin_text=sentence_pinyin,
                        meaning=sentence_meaning,
                    )
                    db.session.add(example)
                    db.session.flush()  # Đảm bảo lấy id của example mới

                else:
                    # Nếu câu đã tồn tại, sử dụng câu đó
                    example = existing_example

                # Tạo liên kết từ và câu
                if not ExampleLink.query.filter_by(
                    vocab_id=vocab_entry.id, example_id=example.id
                ).first():
                    example_link = ExampleLink(
                        vocab_id=vocab_entry.id, example_id=example.id
                    )
                    db.session.add(example_link)
                break  # Thêm một ví dụ cho mỗi từ

    db.session.commit()
    return new_words


def process_text_file(file_path, user):
    """
    Đọc nội dung của file văn bản và phân tích từ mới cho người dùng.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return analyze_text(content, user)
    except FileNotFoundError:
        print("File không tồn tại.")
        return []
