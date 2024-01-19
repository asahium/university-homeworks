#include "lib.h"
#ifndef FLAG
#define FLAG "Invalid flag"
#endif

void handler(u_char*, const struct pcap_pkthdr*, const u_char*);
void send_chat_message(pcap_t* pcap, const char* dest_mac, const char* message, int message_size, int type);

int main(int argc, char** argv)
{
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *alldevs, *p;
    size_t if_len;
    char* mac;
    int i;
    pcap_t* h;
    user_data u;

    init();
    memset(errbuf, 0, PCAP_ERRBUF_SIZE);

    if (argc < 2) {
        printf("Usage: %s <interface>\n", *argv);
        return 0;
    }

    argv++;
    if_len = strlen(*argv);

    if (pcap_init(PCAP_CHAR_ENC_UTF_8, errbuf) == PCAP_ERROR) {
        printf("pcap_init error: %s\n", errbuf);
        return 1;
    }

    if (pcap_findalldevs(&alldevs, errbuf) == PCAP_ERROR) {
        printf("pcap_findalldevs error: %s\n", errbuf);
        return 2;
    }

    for (p = alldevs; p != NULL; p = p->next) {
        if (strncmp(p->name, *argv, if_len) == 0) {
            pcap_addr_t* addr = p->addresses;
            printf("Device %s was found\n", p->name);
            goto dev_found;
        }
    }

    printf("Device %s was not found\n", *argv);
    return 2;

dev_found:
    pcap_freealldevs(alldevs);

    if ((mac = get_mac_address(*argv)) == NULL) {
        printf("Mac address not found, exiting\n");
        return 2;
    }

    printf("mac address for the device is %s\n", mac_to_str(mac));

    if ((h = pcap_create(*argv, errbuf)) == NULL) {
        printf("pcap_create failed: %s\n", errbuf);
        return 3;
    }

    pcap_set_promisc(h, 0);
    pcap_set_immediate_mode(h, 1);
    pcap_set_snaplen(h, SNAPLEN);

    u.pcap = h;
    u.mac = mac;

    if (pcap_activate(h) < 0) {
        pcap_perror(h, "pcap_activate failed :(");
        return 4;
    }

    // Inside the pcap_loop loop, after handling incoming messages
    // Add a section to read user input and send messages
    while (1) {
        char message[256];
        printf("Type your message (or 'exit' to quit): ");
        fgets(message, sizeof(message), stdin);

        if (strcmp(message, "exit\n") == 0) {
            break;
        }

        // Remove the newline character from the end of the message
        message[strcspn(message, "\n")] = '\0';

        // Send a public message (change TYPE_PUBLIC to TYPE_PRIVATE for private messages)
        send_chat_message(h, mac, message, strlen(message), TYPE_PUBLIC);
    }

    // Clean up and exit
    pcap_close(h);
    free(mac);
    return 0;
}

void send_chat_message(pcap_t* pcap, const char* dest_mac, const char* message, int message_size, int type) {
    // Create a chat message
    chat_message msg;
    strncpy(msg.from, "client", sizeof(msg.from));
    strncpy(msg.msg, message, sizeof(msg.msg));
    msg.msg_size = message_size;
    msg.type = type;
    msg.crc = calc_crc(msg.from, msg.msg, msg.msg_size);

    // Send the message
    send_message(pcap, dest_mac, dest_mac, &msg);
}

void handler(u_char *user, const struct pcap_pkthdr *header, const u_char *packet) {
  user_data *data = (user_data *)user;
  struct ether_header *h = (struct ether_header *)packet;
  chat_message *msg;
  if(memcmp(h->ether_dhost, data->mac, 6) != 0) {
    return;
  }
  if(h->ether_type != ether_type) {
    return;
  }
  printf("Incoming package from %s\n", mac_to_str(h->ether_shost));
  msg = (chat_message *)(packet + sizeof(struct ether_header));
  if(msg->crc != calc_crc(msg->from, msg->msg, msg->msg_size)) {
    printf("invalid crc, dropping packet\n");
    return;
  }
  // Vooodooooo magic
  printf("[%*s]->%s: %*s\n", strnlen(msg->from, sizeof(msg->from)), msg->from, (msg->type==TYPE_PUBLIC)?"all":"me", msg->msg_size, msg->msg);
  if(msg->type == TYPE_PUBLIC) { // broadcast this message now
    u_char bcast[] = {0xff,0xff,0xff,0xff,0xff,0xff};
    send_message(data->pcap, data->mac, bcast, msg);
    return;
  }
  // Private message to me with flag
  if(strncmp(msg->msg, "getflag", msg->msg_size) == 0) {
    u_char buf[sizeof(chat_message)+sizeof(FLAG)];
    chat_message *m = (chat_message *)buf;
    m->type = TYPE_PRIVATE;
    strncpy(m->from, "server", sizeof(m->from));
    strncpy(m->msg, FLAG, sizeof(FLAG));
    m->msg_size = sizeof(FLAG);
    m->crc = calc_crc(m->from, m->msg, m->msg_size);
    send_message(data->pcap, data->mac, h->ether_shost, m);
  }

}
