class Node:
    def __init__(self, data, next = None, prev = None): 
        self.val = data
        self.next = next
        self.prev = prev
    
class DeletionSet: #circular linked list + array of addresses

    def __init__(self,N=100):

        self.nodeAddress = [None]*N
        self.sentinela = Node(0) # node extra no inicio para poder excluir sem checar

        last = Node(0,prev = self.sentinela)
        self.sentinela.next = last
        self.nodeAddress[0] = last

        for i in range(1,N):
            last.next = Node(i,prev = last)
            
            last = last.next
            
            self.nodeAddress[i] = last
            

        # link the end with the start
        last.next = self.sentinela  
        self.sentinela.prev = last


    # nao apagar elemento ja apagado
    def del_node(self,index):
        node = self.nodeAddress[index]
        #no if
        (node.prev).next = node.next
        (node.next).prev = node.prev
        

    def parse(self) ->list:
        cur = self.sentinela.next
        not_deleted = list()
        while cur != self.sentinela:
            not_deleted.append(cur.val)
            cur = cur.next
        
        return not_deleted


#test code
if __name__ == "__main__":

    S = DeletionSet(10)
    print(S.parse(),'\n')
    while True:
        entrada = input("0: sair\n1: deletar\ncomando:")
        if entrada =='0': break
        else:
            try:
                index = int(input("indice: "))
            except:
                continue
            S.del_node(index)
        print(S.parse(),'\n')