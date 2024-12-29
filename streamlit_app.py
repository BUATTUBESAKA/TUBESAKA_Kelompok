    import time
    import matplotlib.pyplot as plt
    import streamlit as st

    def is_safe(board, row, col, n):
        for i in range(row):
            if board[i][col] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, n)):
            if board[i][j] == 1:
                return False
        return True

    def solve_n_queens_recursive(board, row, n):
        if row >= n:
            return True
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row][col] = 1
                if solve_n_queens_recursive(board, row + 1, n):
                    return True
                board[row][col] = 0
        return False

    def solve_n_queens_iterative(n):
        board = [[0] * n for _ in range(n)]
        stack = []
        row, col = 0, 0

        while row < n:
            while col < n:
                if is_safe(board, row, col, n):
                    board[row][col] = 1
                    stack.append((row, col))
                    row += 1
                    col = 0
                    break
                col += 1
            else:
                if not stack:
                    return None
                row, col = stack.pop()
                board[row][col] = 0
                col += 1

        return board


    def measure_execution_time(n):
        from time import perf_counter

        # Measure recursive time
        recursive_board = [[0 for _ in range(n)] for _ in range(n)]
        start_time = perf_counter()
        solve_n_queens_recursive(recursive_board, 0, n)
        recursive_time = perf_counter() - start_time

        # Measure iterative time
        start_time = perf_counter()
        iterative_board = solve_n_queens_iterative(n)
        iterative_time = perf_counter() - start_time

        # Prioritize displaying the iterative board for visualization
        board_to_display = iterative_board if iterative_board else recursive_board

        return recursive_time, iterative_time, board_to_display

    def draw_board(board):
        n = len(board)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(color='black')
        for row in range(n):
            for col in range(n):
                color = "white" if (row + col) % 2 == 0 else "gray"
                ax.add_patch(plt.Rectangle((col, n - row - 1), 1, 1, color=color))
                if board[row][col] == 1:
                    ax.text(col + 0.5, n - row - 1 + 0.5, "♛", fontsize=24, ha='center', va='center', color='black')
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_aspect('equal')
        return fig

    # Streamlit UI
    st.title("Visualisasi dan Perbandingan Pendekatan N-Queens")

    # Input untuk memilih ukuran papan
    selected_n = st.slider("Pilih ukuran papan (N):", min_value=4, max_value=20, value=8, step=1)

    # Hitung waktu eksekusi untuk rentang ukuran papan
    n_values = list(range(4, selected_n + 1))
    recursive_times = []
    iterative_times = []
    solution_board = None

    with st.spinner(f"Menghitung solusi dan waktu eksekusi untuk ukuran papan hingga {selected_n}..."):
        for size in n_values:
            recursive_time, iterative_time, board_to_display = measure_execution_time(size)
            recursive_times.append(recursive_time)
            iterative_times.append(iterative_time)
            if size == selected_n:
                solution_board = board_to_display

    # Tampilkan waktu eksekusi untuk ukuran papan terpilih
    st.subheader("Waktu Eksekusi untuk Ukuran Papan yang Dipilih")
    st.write(f"Waktu eksekusi rekursif: {recursive_times[-1]:.6f} detik")
    st.write(f"Waktu eksekusi iteratif: {iterative_times[-1]:.6f} detik")

    # Visualisasi papan solusi
    st.subheader("Papan Solusi")
    if solution_board:
        fig = draw_board(solution_board)
        st.pyplot(fig)
    else:
        st.write("Tidak ada solusi ditemukan.")

    # Visualisasi grafik garis
    st.subheader("Grafik Perbandingan Waktu Eksekusi")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(n_values, recursive_times, label="Rekursif (detik)", marker="o", markersize=3)
    ax.plot(n_values, iterative_times, label="Iteratif (detik)", marker="o", markersize=3)
    ax.set_xlabel("Ukuran Papan (N)")
    ax.set_ylabel("Waktu Eksekusi (detik)")
    ax.set_title("Perbandingan Waktu Eksekusi Pendekatan Rekursif dan Iteratif")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
