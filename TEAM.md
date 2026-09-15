# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm:Hoàng Anh Minh
- Người đại diện / MSSV:Nguyễn Hoàng Anh Minh -2A202602566
- Tên repo: K4-Day04-hoang-anh-minh-2A202602566

- URL repo, nhánh nộp, commit chốt:https://github.com/Minhg14/K4-Day04-hoang-anh-minh-2A202602566.git
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |

| hoàng anh minh| 2A202602566 |Minhg14 | Build | all |

## Nhận xét chung
Kết quả và bằng chứng:

Thiết lập thành công chu trình ReAct Tool-Calling qua OpenRouter/Gemini, kết nối các tools mô phỏng hệ thống Helpdesk (check_service_status, get_device_status, v.v.).

Bằng chứng thực thi: Khi người dùng gửi prompt "Kiểm tra VPN giúp tôi", Agent tự động nhận diện intent check_service_status, gọi tool với đối số service="vpn", trích xuất chính xác mã sự cố INC-1042 kèm khuyến nghị xử lý tạm thời và hiển thị trực quan trên Web UI Streamlit.

Vượt qua bộ kiểm thử tự động run_eval.py sau khi chuẩn hóa cấu trúc dữ liệu eval_group.json theo đúng schema của framework.

Thay đổi hiệu quả nhất:

Chuyển đổi linh hoạt nhà cung cấp sang openrouter và khắc phục header xác thực của API key, giúp vượt qua rào cản hạn ngạch (429 insufficient_quota) và lỗi xác thực token (401 ACCESS_TOKEN_TYPE_UNSUPPORTED).

Xây dựng giao diện Streamlit (app.py) tích hợp sâu vào vòng lặp run_model_tool_loop và quản lý phiên hội thoại chat_history, giúp quan sát trực tiếp các sự kiện gọi tool (Tool Events) theo thời gian thực thay vì giao diện console tĩnh.

Giới hạn còn lại:

Dữ liệu mô phỏng trong tools.py còn giới hạn về số lượng bản ghi định danh (ví dụ: máy LAPTOP-HN-042 không tồn tại trong mock DB dẫn đến kết quả rỗng).

Phản hồi từ Agent hiện tại xuất ra định dạng JSON có cấu trúc phục vụ chấm điểm ({"intent": ..., "reply": ...}), chưa được bóc tách hoàn toàn sang ngôn ngữ tự nhiên thuần túy trên giao diện người dùng cuối.

Cách phân công và tích hợp:

Chuẩn hóa bộ dữ liệu test case và validation schema (eval_group.json).

Cấu hình tích hợp LLM Provider và đồng bộ biến môi trường qua file .env.

Thiết kế và ghép nối luồng xử lý Web UI Streamlit với engine xử lý hội thoại đa lượt trong chat.py.

## INDIVIDUAL

Hoang Anh Minh — 2A202602566
Phần việc và file/commit/PR:

Thiết lập và kiểm thử bộ test suite đánh giá: cấu hình và chỉnh sửa file starter_v0/data/eval_group.json.

Xử lý tương thích Provider và môi trường: cấu hình starter_v0/providers/gemini_provider.py và .env.

Phát triển giao diện Web Chat tương tác: xây dựng file starter_v0/app.py kết nối trực tiếp chu trình run_model_tool_loop từ starter_v0/chat.py.

Cập nhật tài liệu phụ thuộc: bổ sung thư viện streamlit>=1.30.0 vào starter_v0/requirements.txt.

Quyết định, khó khăn và cách xử lý:

Khó khăn 1: Script run_eval.py liên tục báo lỗi KeyError: 'phase', ValueError: Invalid failure_type, và KeyError: 'expect' do dữ liệu test case thiếu các trường quy chuẩn.

Cách xử lý: Tái cấu trúc lại file eval_group.json, bổ sung đồng bộ trường phase="B", gán các giá trị failure_type hợp lệ (wrong_arg_value, missing_info, wrong_tool,...) và bọc cấu trúc mong đợi vào object expect.

Khó khăn 2: Lỗi 401 ACCESS_TOKEN_TYPE_UNSUPPORTED khi gọi Gemini do token dạng mới (AQ...) và lỗi cạn kiệt quota 429 của OpenAI.

Cách xử lý: Chuyển đổi provider sang openrouter bằng cách nạp OPENROUTER_API_KEY, đồng thời điều chỉnh lại cơ chế header auth để đảm bảo khả năng dự phòng (fallback).

Khó khăn 3: Giao diện Streamlit ban đầu chỉ phản hồi tĩnh mà không thực thi logic Agent, kết hợp với lỗi môi trường ảo terminal không nhận package.

Cách xử lý: Kích hoạt đúng .venv/Scripts/Activate.ps1, import trực tiếp run_model_tool_loop và logic quản lý lịch sử trim_history vào app.py để đồng bộ hoàn toàn với chat.py.

Điều đã học:

Hiểu rõ cơ chế hoạt động của Agentic Tool-Calling: từ khâu phân tích ý định (intent parsing), sinh schema gọi hàm (Function Calling), bắt lỗi ranh giới (boundary/failure types), đến việc nạp ngược tool_results vào LLM context.

Kỹ năng gỡ lỗi hệ thống tích hợp đa nền tảng (LLM API keys, rate limits, virtual environments và session state trong Streamlit).

AI/công cụ đã dùng và cách kiểm tra:

Công cụ: VS Code (Antigravity IDE), Python 3.11, PowerShell, Streamlit, Git.

Hỗ trợ AI: Gemini / OpenAI để phân tích nguyên nhân Traceback lỗi cú pháp schema JSON và hỗ trợ viết boilerplate kết nối Streamlit.

Cách kiểm tra: Chạy lệnh nghiệm thu run_eval.py, test thủ công luồng chat qua terminal (chat.py) và kiểm chứng trực quan các lượt tương tác tra cứu VPN, kiểm tra thiết bị qua Web UI (streamlit run app.py).

Thời điểm đã tự nộp URL repo chung trên VLearn:

15/09/2026 — Hoàn thành nộp liên kết kho lưu trữ GitHub sau khi đã commit toàn bộ mã nguồn app.py, eval_group.json và kiểm tra hoạt động.