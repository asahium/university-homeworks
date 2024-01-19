#include <stdio.h>
#include <string.h>
#include <pcap.h>
#include "lib.h"

#ifndef FLAG
#define FLAG "Invalid flag"
#endif

#define SNAPLEN 1500
#define ether_type 0x0800

typedef struct {
    pcap_t *pcap;
    char *mac;
} user_data;

void handler(u_char *, const struct pcap_pkthdr *, const u_char *);

int main(int argc, char **argv) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *alldevs, *p;
    size_t if_len;
    char *mac;
    pcap_t *h;
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

    if (pcap_loop(h, -1, handler, (u_char *) &u) == PCAP_ERROR) {
        pcap_perror(h, "pcap_loop failed :(");
    }

    return 0;
}

void handler(u_char *user, const struct pcap_pkthdr *header, const u_char *packet) {
    user_data *data = (user_data *) user;
    struct ether_header *h = (struct ether_header *) packet;
    chat_message *msg;

    if (memcmp(h->ether_dhost, data->mac, 6) != 0 || h->ether_type != ether_type) {
        return;
    }

    printf("Incoming package from %s\n", mac_to_str(h->ether_shost));
    msg = (chat_message *) (packet + sizeof(struct ether_header));

    if (msg->crc != calc_crc(msg->from, msg->msg, msg->msg_size)) {
        printf("invalid crc, dropping packet\n");
        return;
    }

    printf("[%.*s]->%s: %.*s\n", (int) strnlen(msg->from, sizeof(msg->from)), msg->from,
           (msg->type == TYPE_PUBLIC) ? "all" : "me", msg->msg_size, msg->msg);

    if (msg->type == TYPE_PUBLIC) {
        u_char bcast[] = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff};
        send_message(data->pcap, data->mac, bcast, msg);
        return;
    }

    if (strncmp(msg->msg, "getflag", msg->msg_size) == 0) {
        u_char buf[sizeof(chat_message) + sizeof(FLAG)];
        chat_message *m = (chat_message *) buf;
        m->type = TYPE_PRIVATE;
        strncpy(m->from, "server", sizeof(m->from));
        strncpy(m->msg, FLAG, sizeof(FLAG));
        m->msg_size = sizeof(FLAG);
        m->crc = calc_crc(m->from, m->msg, m->msg_size);
        send_message(data->pcap, data->mac, h->ether_shost, m);
    }
}
