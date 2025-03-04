import blockchain
import json
import time
import new_consensus_module
import output
import encryption_module
import modification
import sys
import test_data
import main

class Miner:
    def __init__(self, address, trans_delay, gossiping, uploadBandwidth = 0, downloadBandwidth = 0):
        self.address = "Miner_" + str(address)
        self.top_block = {}
        self.isAuthorized = False
        self.next_pos_block_from = self.address
        self.neighbours = set()
        self.trans_delay = trans_delay/1000
        self.gossiping = gossiping
        self.waiting_times = {}
        self.dpos_vote_for = None
        self.amount_to_be_staked = None
        self.delegates = None
        self.adversary = False
        self.uploadDataUsage = 0
        self.downloadDataUsage = 0
        self.uploadBandwidth = uploadBandwidth
        self.downloadBandwidth = downloadBandwidth

    def build_block(self, num_of_tx_per_block, mempool, miner_list, type_of_consensus, blockchain_function, AI_assisted_mining_wanted, fastPoS = False):
        #print("uploadBandwidth : " + str(self.uploadBandwidth))
        block_time = 0
        if type_of_consensus == 3 and not self.isAuthorized:
            output.unauthorized_miner_msg(self.address)
        elif type_of_consensus == 4:
            waiting_time = (self.top_block['Body']['timestamp'] + self.waiting_times[self.top_block['Header']['blockNo'] + 1]) - time.time()
            if waiting_time <= 0:
                block_time = self.continue_building_block(num_of_tx_per_block, mempool, miner_list, type_of_consensus, blockchain_function, AI_assisted_mining_wanted)
        else:
            #useful code for pos, pow
            block_time = self.continue_building_block(num_of_tx_per_block, mempool, miner_list, type_of_consensus, blockchain_function, AI_assisted_mining_wanted, fastPoS)

        return block_time

    def continue_building_block(self, num_of_tx_per_block, mempool, miner_list, type_of_consensus, blockchain_function, AI_assisted_mining_wanted, fastPoS = False):
        time_start = time.time()
        #print("  ++++++++++++++++++++++++++++ ADAstart:")
        accumulated_transactions = new_consensus_module.accumulate_transactions(num_of_tx_per_block, mempool, blockchain_function,
                                                                                self.address)
        other_miners_time = 0
        if accumulated_transactions:
            transactions = accumulated_transactions
            new_block = self.abstract_block_building(blockchain_function, transactions, miner_list, type_of_consensus, AI_assisted_mining_wanted)
            output.block_info(new_block, type_of_consensus)
            
            #print("miner sleeping (trans_delay):" + str(self.trans_delay) + "secs")
            #time.sleep(self.trans_delay)
            #print("miner wake up")
            
            #print("  ++++++++++++++++++++++++++++ ADB:"+str(time.time() - time_start))
            
            time_before_send = time.time()
            upload_time = 0
            download_time = 0
            for elem in miner_list:
                if elem.address in self.neighbours:
                    blockSize = sys.getsizeof(str(new_block))
                    # print("-------------------------------------------blockSize = " + str(blockSize) + ", block: " + str(new_block))
                    self.uploadDataUsage += blockSize
                    upload_time += blockSize / (float)(self.uploadBandwidth)
                    download_time += blockSize / (float)(self.downloadBandwidth)
                    if not fastPoS:
                        elem.receive_new_block(new_block, type_of_consensus, miner_list, blockchain_function)
                      
            time_cost_of_send = time.time() - time_before_send
            
            # if fastPoS:
                # miner_list[0].receive_new_block(new_block, type_of_consensus, miner_list, blockchain_function) 
            print("+++++++++++++++++++++++++ uploadtime = " + str(upload_time))
            #print("  ++++++++++++++++++++++++++++ ADC:"+str(time.time() - time_start))
        #print("  ++++++++++++++++++++++++++++ ADEend:"+str(time.time() - time_start))
    
        time_cost = time.time() - time_start - time_cost_of_send + upload_time + self.trans_delay + download_time
        test_data.totalDownloadTime += download_time
        test_data.totalUploadTime += upload_time
        test_data.totalNetworkDelayTime += self.trans_delay
        #print("============================  build_time_cost = "+str(time_cost) + " , send_time_cost = " + str(time_cost_of_send))
        
        return time_cost
            

    def abstract_block_building(self, blockchain_function, transactions, miner_list, type_of_consensus, AI_assisted_mining_wanted):
        if blockchain_function == 3:
            transactions = self.validate_transactions(transactions, "generator")
        if self.gossiping:
            self.gossip(blockchain_function, miner_list)
        new_block = new_consensus_module.generate_new_block(transactions, self.address,
                                                            self.top_block['Header']['hash'], type_of_consensus,
                                                            AI_assisted_mining_wanted, self.adversary)
        if type_of_consensus == 4:
            new_block['Header']['PoET'] = encryption_module.retrieve_signature_from_saved_key(
                new_block['Body']['previous_hash'], self.address)
        return new_block

    def receive_new_block(self, new_block, type_of_consensus, miner_list, blockchain_function): #TODO: add start timestamp

        #print("   ++++++++++++++++++++++++++++ ADBA start:")
        
        block_already_received = False
        local_chain_temporary_file = modification.read_file(str("temporary/" + self.address + "_local_chain.json"))
        # print("a new block is received from " + str(new_block['generator_id']))
        condition_1 = (len(local_chain_temporary_file) == 0) and (new_block['Header']['generator_id'] == 'The Network')
        #print("   ++++++++++++++++++++++++++++ ADBB:"+str(time.time() - time_start))
        
        if condition_1:
            self.add(new_block, blockchain_function, miner_list) # this take 0.3sec but this only run when init
            #print("   ++++++++++++++++++++++++++++ ADBC:"+str(time.time() - time_start))
            
        else:
            if self.gossiping:
                self.gossip(blockchain_function, miner_list) # this take 0.2sec and cause delay during simulation
                #print("   ++++++++++++++++++++++++++++ ADBD:"+str(time.time() - time_start))
                
            list_of_hashes_in_local_chain = []
            for key in local_chain_temporary_file:
                read_hash = local_chain_temporary_file[key]['Header']['hash']
                list_of_hashes_in_local_chain.append(read_hash)
                if new_block['Header']['hash'] == read_hash:
                    block_already_received = True
                    break
            
            #print("   ++++++++++++++++++++++++++++ ADBE:"+str(time.time() - time_start))
            if not block_already_received:
                self.downloadDataUsage += sys.getsizeof(new_block)
                if new_consensus_module.block_is_valid(type_of_consensus, new_block, self.top_block, self.next_pos_block_from, miner_list, self.delegates):
                    self.add(new_block, blockchain_function, miner_list)
                    #print("miner sleeping (trans_delay):" + str(self.trans_delay) + "secs")
                    #time.sleep(self.trans_delay)
                    #print("miner wake up")
                    if main.fastPoS:
                        return
                    for elem in miner_list:
                        if elem.address in self.neighbours:
                            self.uploadDataUsage += sys.getsizeof(new_block)
                            elem.receive_new_block(new_block, type_of_consensus, miner_list, blockchain_function)

                
            #print("   ++++++++++++++++++++++++++++ ADBF end:"+str(time.time() - time_start))
            

    def validate_transactions(self, list_of_new_transactions, miner_role):
        user_wallets_temporary_file = modification.read_file(str("temporary/" + self.address + "_users_wallets.json"))
        if list_of_new_transactions:
            for key in user_wallets_temporary_file:
                for transaction in list_of_new_transactions:
                    if miner_role == "receiver":
                        if key == (str(transaction[1]) + "." + str(transaction[2])):
                            if user_wallets_temporary_file[key]['wallet_value'] >= transaction[0]:
                                user_wallets_temporary_file[key]['wallet_value'] -= transaction[0]
                            else:
                                return False
                        if key == (str(transaction[3]) + "." + str(transaction[4])):
                            user_wallets_temporary_file[key]['wallet_value'] += transaction[0]
                    if miner_role == "generator" and key == (str(transaction[1]) + "." + str(transaction[2])):
                        if user_wallets_temporary_file[key]['wallet_value'] < transaction[0]:
                            output.illegal_tx(transaction, user_wallets_temporary_file[key]['wallet_value'])
                            del transaction
        if miner_role == "generator":
            return list_of_new_transactions
        if miner_role == "receiver":
            modification.rewrite_file(str("temporary/" + self.address + "_users_wallets.json"), user_wallets_temporary_file)
            return True

    def add(self, block, blockchain_function, list_of_miners):
        ready = False
        local_chain_temporary_file = modification.read_file("temporary/" + self.address + "_local_chain.json")
        if len(local_chain_temporary_file) == 0:
            ready = True
        else:          
            condition = blockchain_function == 3 and self.validate_transactions(block['Body']['transactions'], "receiver")
            if blockchain_function != 3 or condition:
                if block['Body']['previous_hash'] == self.top_block['Header']['hash']:
                    blockchain.report_a_successful_block_addition(block['Header']['generator_id'], block['Header']['hash'])
                    # output.block_success_addition(self.address, block['generator_id'])
                    ready = True
        if ready:
            block['Header']['blockNo'] = len(local_chain_temporary_file)
            self.top_block = block
            local_chain_temporary_file[str(len(local_chain_temporary_file))] = block
            modification.rewrite_file(str("temporary/" + self.address + "_local_chain.json"), local_chain_temporary_file)
            if self.gossiping:
                self.update_global_longest_chain(local_chain_temporary_file, blockchain_function, list_of_miners)

    def gossip(self, blockchain_function, list_of_miners): #TODO: add start timestamp
        local_chain_temporary_file = modification.read_file(str("temporary/" + self.address + "_local_chain.json"))
        temporary_global_longest_chain = modification.read_file('temporary/longest_chain.json')
        condition_1 = len(temporary_global_longest_chain['chain']) > len(local_chain_temporary_file)
        condition_2 = self.global_chain_is_confirmed_by_majority(temporary_global_longest_chain['chain'], len(list_of_miners))
        if condition_1 and condition_2:
            confirmed_chain = temporary_global_longest_chain['chain']
            confirmed_chain_from = temporary_global_longest_chain['from']
            modification.rewrite_file(str("temporary/" + self.address + "_local_chain.json"), confirmed_chain)
            self.top_block = confirmed_chain[str(len(confirmed_chain) - 1)]
            output.local_chain_is_updated(self.address, len(confirmed_chain))
            if blockchain_function == 3:
                user_wallets_temp_file = modification.read_file(str("temporary/" + confirmed_chain_from + "_users_wallets.json"))
                modification.rewrite_file(str("temporary/" + self.address + "_users_wallets.json"), user_wallets_temp_file)

    def global_chain_is_confirmed_by_majority(self, global_chain, no_of_miners):
        chain_is_confirmed = True
        temporary_confirmations_log = modification.read_file('temporary/confirmation_log.json')
        for block in global_chain:
            condition_0 = block != '0'
            if condition_0:
                condition_1 = not (global_chain[block]['Header']['hash'] in temporary_confirmations_log)
                if condition_1:
                    chain_is_confirmed = False
                    break
                else:
                    condition_2 = temporary_confirmations_log[global_chain[block]['Header']['hash']]['votes'] <= (no_of_miners / 2)
                    if condition_2:
                        chain_is_confirmed = False
                        break
        return chain_is_confirmed

    def update_global_longest_chain(self, local_chain_temporary_file, blockchain_function, list_of_miners):
        temporary_global_longest_chain = modification.read_file('temporary/longest_chain.json')
        if len(temporary_global_longest_chain['chain']) < len(local_chain_temporary_file):
            temporary_global_longest_chain['chain'] = local_chain_temporary_file
            temporary_global_longest_chain['from'] = self.address
            modification.rewrite_file('temporary/longest_chain.json', temporary_global_longest_chain)
        else:
            if len(temporary_global_longest_chain['chain']) > len(local_chain_temporary_file) and self.gossiping:
                self.gossip(blockchain_function, list_of_miners)
