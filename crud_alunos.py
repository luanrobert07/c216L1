alunos = {}
contadores_curso = {}
contador_matricula = 0


def gerar_matricula(curso):
    curso = curso.upper()

    if curso not in contadores_curso:
        contadores_curso[curso] = 1
    else:
        contadores_curso[curso] += 1

    return f"{curso}{contadores_curso[curso]}"


def cadastrar_aluno():
    print("\nCadastrar Aluno")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    curso = input("Curso (ex: GES, GEC, GET, GEP): ").strip().upper()

    matricula = gerar_matricula(curso)

    alunos[matricula] = {
        "nome": nome,
        "email": email,
        "curso": curso,
        "matricula": matricula,
    }

    print(f"Aluno cadastrado com sucesso! Matrícula: {matricula}")


def listar_alunos():
    print("\nLista de Alunos")

    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for matricula, dados in alunos.items():
        print(f"\nMatrícula: {dados['matricula']}")
        print(f"Nome: {dados['nome']}")
        print(f"Email: {dados['email']}")
        print(f"Curso: {dados['curso']}")


def buscar_aluno():
    print("\nBuscar Aluno")
    matricula = input("Digite a matrícula do aluno: ").strip().upper()

    if matricula in alunos:
        dados = alunos[matricula]
        print(f"\nMatrícula: {dados['matricula']}")
        print(f"Nome: {dados['nome']}")
        print(f"Email: {dados['email']}")
        print(f"Curso: {dados['curso']}")
    else:
        print("Aluno não encontrado.")


def atualizar_aluno():
    print("\nAtualizar Aluno")
    matricula = input("Digite a matrícula do aluno: ").strip().upper()

    if matricula in alunos:
        print("Deixe em branco para manter o valor atual.")

        novo_nome = input(f"Novo nome ({alunos[matricula]['nome']}): ").strip()
        novo_email = input(f"Novo email ({alunos[matricula]['email']}): ").strip()
        novo_curso = (
            input(f"Novo curso ({alunos[matricula]['curso']}): ").strip().upper()
        )

        if novo_nome:
            alunos[matricula]["nome"] = novo_nome
        if novo_email:
            alunos[matricula]["email"] = novo_email
        if novo_curso:
            alunos[matricula]["curso"] = novo_curso

        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")


def remover_aluno():
    print("\nRemover Aluno")
    matricula = input("Digite a matrícula do aluno: ").strip().upper()

    if matricula in alunos:
        del alunos[matricula]
        print("Aluno removido com sucesso!")
    else:
        print("Aluno não encontrado.")


def exibir_menu():
    print("\nMENU")
    print("1. Cadastrar aluno")
    print("2. Listar alunos")
    print("3. Buscar aluno")
    print("4. Atualizar aluno")
    print("5. Remover aluno")
    print("6. Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            buscar_aluno()
        elif opcao == "4":
            atualizar_aluno()
        elif opcao == "5":
            remover_aluno()
        elif opcao == "6":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
